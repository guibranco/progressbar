import codecs
import ipaddress
import json
import re
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from flask import Flask, make_response, redirect, render_template, request
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

app = Flask(__name__)


def _select_autoescape(template_name):
  if template_name is None:
    return True
  return template_name.endswith((".html", ".htm", ".xml", ".xhtml", ".svg"))


app.jinja_env.autoescape = _select_autoescape

JSON_FETCH_MAX_BYTES = 512 * 1024
JSON_FETCH_TIMEOUT_SEC = 8
JSON_FETCH_USER_AGENT = "progressbar-dynamic-json/1.0"
JSON_URL_MAX_LENGTH = 2048

# Reject obvious non-JSON / active content when Content-Type is present.
_JSON_FETCH_BLOCK_CT_PREFIXES = (
  "text/html",
  "application/xhtml",
  "image/",
  "video/",
  "audio/",
  "application/javascript",
  "text/javascript",
  "multipart/",
  "application/zip",
  "application/gzip",
  "application/x-gzip",
)


class _NoHttpRedirectHandler(HTTPRedirectHandler):
  """Do not follow redirects (blocks SSRF via Location: http://127.0.0.1/...)."""

  def redirect_request(self, req, fp, code, msg, headers, newurl):
    raise URLError("http redirect not allowed")


_fetch_json_opener = build_opener(_NoHttpRedirectHandler)


def _content_type_allowed_for_json_fetch(content_type_header):
  if not content_type_header:
    return True
  ct = content_type_header.split(";")[0].strip().lower()
  return not any(ct.startswith(p) for p in _JSON_FETCH_BLOCK_CT_PREFIXES)


def _charset_from_content_type(content_type_header):
  """Return a Python codec name from Content-Type charset=..., default utf-8."""
  if not content_type_header:
    return "utf-8"
  m = re.search(r"charset\s*=\s*([^;\s]+)", content_type_header, flags=re.I)
  if not m:
    return "utf-8"
  raw = m.group(1).strip().strip('"').strip("'")
  if raw.lower() in ("utf8", "utf_8"):
    return "utf-8"
  return raw


def _decode_json_bytes(content_type_header, data):
  encoding = _charset_from_content_type(content_type_header or "")
  try:
    codecs.lookup(encoding)
  except LookupError as e:
    raise ValueError(f"unsupported charset: {encoding}") from e
  return data.decode(encoding)


def _ip_for_ssrf_check(addr):
  ip = ipaddress.ip_address(addr)
  if ip.version == 6 and ip.ipv4_mapped is not None:
    return ip.ipv4_mapped
  return ip


def _finalize_svg_response(response):
  response.headers["Content-Type"] = "image/svg+xml"
  response.headers["X-Content-Type-Options"] = "nosniff"
  return response


def normalize_jsonpath_query(selector):
  """JSONPath ($.items[0].metrics.pct) or dot path from root (items.0.metrics.pct)."""
  q = (selector or "").strip()
  if not q:
    raise ValueError("empty query")
  if q.startswith("$"):
    return q
  parts = [p for p in q.split(".") if p != ""]
  if not parts:
    raise ValueError("empty query")
  out = "$"
  for p in parts:
    if p.isdigit():
      out += f"[{p}]"
    elif out == "$":
      out = "$." + p
    else:
      out += "." + p
  return out


def url_is_allowed_for_fetch(url):
  if not url or len(url) > JSON_URL_MAX_LENGTH:
    return False
  parsed = urlparse(url)
  if parsed.scheme not in ("http", "https"):
    return False
  if parsed.username or parsed.password:
    # e.g. http://127.0.0.1@evil.com/ looks public but embeds a misleading host.
    return False
  port = parsed.port
  if port is not None and port not in (80, 443):
    return False
  host = (parsed.hostname or "").lower()
  if not host:
    return False
  blocked_hosts = (
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "metadata.google.internal",
    "metadata.goog",
  )
  if host in blocked_hosts or host.endswith(".localhost"):
    return False
  if "169.254.169.254" in host:
    return False
  host_for_ip = host.strip("[]")
  try:
    ip = _ip_for_ssrf_check(host_for_ip)
    if (
      ip.is_private
      or ip.is_loopback
      or ip.is_link_local
      or ip.is_reserved
      or ip.is_multicast
    ):
      return False
  except ValueError:
    pass
  try:
    for res in socket.getaddrinfo(host, None):
      addr = res[4][0]
      try:
        ip = _ip_for_ssrf_check(addr)
        if (
          ip.is_private
          or ip.is_loopback
          or ip.is_link_local
          or ip.is_reserved
          or ip.is_multicast
        ):
          return False
      except ValueError:
        continue
  except OSError:
    return False
  return True


def fetch_json_document(url):
  req = Request(
    url,
    headers={"User-Agent": JSON_FETCH_USER_AGENT},
    method="GET",
  )
  with _fetch_json_opener.open(req, timeout=JSON_FETCH_TIMEOUT_SEC) as resp:
    ct_header = resp.headers.get("Content-Type")
    if not _content_type_allowed_for_json_fetch(ct_header):
      raise ValueError("unsupported content type")
    data = resp.read(JSON_FETCH_MAX_BYTES + 1)
  if len(data) > JSON_FETCH_MAX_BYTES:
    raise ValueError("response too large")
  text = _decode_json_bytes(ct_header, data)
  return json.loads(text)


def extract_progress_with_jsonpath(doc, selector):
  path = normalize_jsonpath_query(selector)
  try:
    expr = parse(path)
  except JsonPathParserError as e:
    raise ValueError(f"invalid JSONPath: {e}") from e
  matches = [m.value for m in expr.find(doc)]
  if not matches:
    raise ValueError("JSONPath matched no values")
  raw = matches[0]
  if isinstance(raw, bool):
    raise ValueError("matched value is boolean")
  if isinstance(raw, (int, float)):
    return float(raw)
  if isinstance(raw, str):
    s = raw.strip()
    if not s:
      raise ValueError("matched string is empty")
    if s.endswith("%"):
      s = s[:-1].strip()
    try:
      return float(s)
    except ValueError as e:
      raise ValueError("matched string is not numeric") from e
  raise ValueError("matched value is not numeric")


def error_svg_response(message, status=502):
  template = render_template("dynamic_error.svg", message=message)
  response = make_response(template, status)
  return _finalize_svg_response(response)

def is_true(value):
  return value.lower() == 'true'

def get_progress_color(progress, scale):
    """Get the color representation of progress based on a scale.

    This function calculates the ratio of progress to scale and returns a
    color code that represents the level of progress. The color codes are
    defined as follows: - Red ("d9534f") for progress less than 30% - Yellow
    ("f0ad4e") for progress between 30% and 70% - Green ("5cb85c") for
    progress of 70% or more.

    Args:
        progress (float): The current progress value.
        scale (float): The maximum scale value to compare against.

    Returns:
        str: A hex color code representing the progress level.
    """

    ratio = progress/scale

    if ratio < 0.3:
        return "d9534f"
    if ratio < 0.7:
        return "f0ad4e"

    return "5cb85c"

def get_style_fields(style):
    """Retrieve style fields based on the specified style type.

    This function returns a dictionary of style properties associated with
    the given style name. It checks a predefined set of style templates and
    returns the corresponding style configuration. If the specified style
    does not exist, it returns an empty dictionary.

    Args:
        style (str): The name of the style for which to retrieve fields.

    Returns:
        dict: A dictionary containing style properties for the specified style,
            or an empty dictionary if the style is not found.
    """

    style_templates = {
        "default": {
            "title": "",
            "title_width": 0,
            "title_color": "428bca",
            "scale": 100,
            "progress_width": 60,
            # "progress_color": "5cb85c",
            "progress_background": "555",
            "progress_number_color": "fff",
            "prefix": "",
            "suffix": "%",
            "show_text": True,
            "show_shadow": True,
            "border_radius": 4,
            "as_percent": False,
            "letter_spacing": 0,
            "font_size": 11,
            "height": 20,
            "progress_weight": "normal",
            "title_weight": "normal",
            "title_anchor": "left",
            "gradient": True,
        },
        "flat": {
        },
        "square": {
            "border_radius": 0,
            "title_color": "555",
            "progress_color": "97CA00",
            "show_shadow": False,
        },
        "plastic": {
            "border_radius": 5,
            "title_color": "555",
            "progress_color": "91bc13",  # Greenish color for a plastic look
            "progress_background": "ECEFF1",  # Light background to enhance contrast
            "show_shadow": True,
            "gloss": True,  # Adding a gloss effect for plastic
        },
        "for-the-badge": {
            "border_radius": 0,
            "title_width": 10,
            "title_color": "555",
            "progress_weight": "bold",
            "progress_color": "97ca00",
            "show_shadow": False,
            "letter_spacing": 2,
            "font_size": 10,
            "height": 28,
            "title_anchor": "middle",
            "gradient": False,
        },
    }
    return style_templates.get(style) if style in style_templates else {}

def get_template_fields(progress):
    """Retrieve template fields for rendering progress information.

    This function extracts various parameters from the request arguments,
    including the title, scale, and width for the progress display. It also
    sets default values for these parameters if they are not provided or if
    there are errors in conversion. The function returns a dictionary
    containing all the necessary fields to render a progress template.

    Args:
        progress (int): The current progress value to be displayed.

    Returns:
        dict: A dictionary containing the template fields, including title,
            title width, colors, scale, progress value, and other related
            parameters for rendering the progress template.
    """

    title = request.args.get("title")

    progress_text = progress

    scale = 100
    try:
        scale = int(request.args.get("scale"))
        if request.args.get("as_percent"):
            progress_text = int(progress / scale * 100)
    except (TypeError, ValueError):
        pass

    progress_width = 60 if title else 90
    try:
        progress_width = int(request.args.get("width"))
    except (TypeError, ValueError):
        pass

    show_text = request.args.get('show_text', type=is_true)
    show_shadow = request.args.get('show_shadow', type=is_true)

    req_params = {
        "title": title,
        "title_color": request.args.get("color"),
        "scale": scale,
        "progress": progress,
        "progress_text": progress_text,
        "progress_width": progress_width,
        "progress_color": request.args.get("progress_color"),
        "progress_background": request.args.get("progress_background"),
        "progress_number_color": request.args.get("progress_number_color"),
        "prefix": request.args.get("prefix"),
        "suffix": request.args.get("suffix"),
        "show_text": show_text,
        "show_shadow": show_shadow,
        "border_radius": request.args.get("radius"),
    }

    default = get_style_fields("default")
    style = {**default, **get_style_fields(request.args.get("style"))}
    clean_req_params = {k: v for k, v in req_params.items() if v is not None}

    # fields that need to be calculated based on other fields

    if "title" in clean_req_params and clean_req_params["title"] != "":
        clean_req_params["title_width"] = (
            style.get("title_width")
            + 10 + (6 * len(clean_req_params["title"]))
            + (len(clean_req_params["title"]) * style.get("letter_spacing", 1))
        )
    else:
        clean_req_params["title_width"] = 0

    if "progress_color" not in clean_req_params:
        clean_req_params["progress_color"] = style.get("progress_color") or default.get(
            "progress_color", get_progress_color(progress, scale)
        )

    if style.get("title_anchor") == "left":
        clean_req_params["title_pos_x"] = 5
        clean_req_params["title_pos_y"] = 14
    elif style.get("title_anchor") == "middle":
        clean_req_params["title_pos_x"] = clean_req_params.get("title_width", 0) / 2
        clean_req_params["title_pos_y"] = 18

    return {**style, **clean_req_params}


@app.route("/dynamic/json/")
def get_progress_svg_dynamic_json():
  """Load progress from a remote JSON `url` and a `query` into that document.

  `query` is JSONPath (e.g. $.items[0].metrics.pct) or dot form from the root
  (e.g. items.0.metrics.pct).
  Optional `cache` sets Cache-Control max-age in seconds.
  Other params match /N/ (title, scale, width, style, …).
  """
  json_url = request.args.get("url")
  json_query = request.args.get("query")
  if not json_url or not json_query:
    return error_svg_response("missing url or query", 400)
  if not url_is_allowed_for_fetch(json_url):
    return error_svg_response("url not allowed", 400)
  try:
    doc = fetch_json_document(json_url)
    progress = extract_progress_with_jsonpath(doc, json_query)
  except (URLError, HTTPError, TimeoutError, OSError):
    return error_svg_response("fetch failed", 502)
  except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as e:
    msg = str(e)[:60] if str(e) else "bad json or query"
    return error_svg_response(msg, 422)

  template_fields = get_template_fields(progress)
  template = render_template("progress.svg", **template_fields)
  response = make_response(template)
  response = _finalize_svg_response(response)
  cache_raw = request.args.get("cache") or request.args.get("cacheSeconds")
  if cache_raw is not None:
    try:
      sec = max(0, min(int(cache_raw), 86400))
      if sec > 0:
        response.headers["Cache-Control"] = f"public, max-age={sec}"
    except (TypeError, ValueError):
      pass
  return response


@app.route("/<int:progress>/")
def get_progress_svg(progress):
    template_fields = get_template_fields(progress)

    template = render_template("progress.svg", **template_fields)

    response = make_response(template)
    return _finalize_svg_response(response)

@app.route("/")
def redirect_to_github():
    return redirect("https://github.com/guibranco/progressbar", code=302)

if __name__ == "__main__":
    app.run()
