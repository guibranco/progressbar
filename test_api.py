import json
import re
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest
import app as app_module
from app import (
    DYNAMIC_JSON_CACHE_SECONDS,
    JSON_FETCH_MAX_BYTES,
    JSON_URL_MAX_LENGTH,
    MAX_CACHE_SECONDS,
    STALE_WHILE_REVALIDATE_SECONDS,
    STATIC_CACHE_SECONDS,
    app,
    cache_control_value,
    fetch_json_document,
    get_fill_geometry,
    parse_progress_origin,
)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_svg_response(client):
    response = client.get("/28/")

    assert response.status_code == 200

    assert response.content_type == "image/svg+xml"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"

    assert b"<svg" in response.data
    assert b"</svg>" in response.data


def test_static_badge_is_cacheable(client):
    response = client.get("/28/", query_string={"title": "progress", "style": "flat"})
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == (
        f"public, max-age={STATIC_CACHE_SECONDS}, s-maxage={STATIC_CACHE_SECONDS}, "
        f"stale-while-revalidate={STALE_WHILE_REVALIDATE_SECONDS}"
    )


def test_static_badge_cache_can_be_tuned(client, monkeypatch):
    monkeypatch.setattr(app_module, "STATIC_CACHE_SECONDS", 120)
    response = client.get("/28/")
    assert response.headers.get("Cache-Control").startswith("public, max-age=120, s-maxage=120")


def test_static_badge_defines_clip_paths(client):
    response = client.get("/28/", query_string={"title": "clip", "style": "plastic"})
    assert response.status_code == 200
    assert b'<clipPath id="clip">' in response.data
    assert b'<clipPath id="progress_clip">' in response.data


def test_framework_errors_are_not_cacheable(client):
    response = client.get("/not-a-route/")
    assert response.status_code == 404
    assert response.headers.get("Cache-Control") == "no-store"

    response = client.post("/health")
    assert response.status_code == 405
    assert response.headers.get("Cache-Control") == "no-store"


def test_health(client):
    for path in ("/health", "/health/"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}
        assert response.headers.get("Cache-Control") == "no-store"


def test_favicon(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.mimetype == "image/vnd.microsoft.icon"
    assert "max-age=86400" in response.headers["Cache-Control"]


def test_env_int_parsing(monkeypatch):
    monkeypatch.setenv("PROGRESSBAR_TEST_INT", "900")
    assert app_module._env_int("PROGRESSBAR_TEST_INT", 5) == 900
    monkeypatch.setenv("PROGRESSBAR_TEST_INT", "999999")
    assert app_module._env_int("PROGRESSBAR_TEST_INT", 5) == MAX_CACHE_SECONDS
    monkeypatch.setenv("PROGRESSBAR_TEST_INT", "-1")
    assert app_module._env_int("PROGRESSBAR_TEST_INT", 5) == 0
    monkeypatch.setenv("PROGRESSBAR_TEST_INT", "abc")
    assert app_module._env_int("PROGRESSBAR_TEST_INT", 5) == 5
    monkeypatch.setenv("PROGRESSBAR_TEST_INT", "")
    assert app_module._env_int("PROGRESSBAR_TEST_INT", 5) == 5
    monkeypatch.delenv("PROGRESSBAR_TEST_INT")
    assert app_module._env_int("PROGRESSBAR_TEST_INT", 5) == 5


def test_cache_control_value():
    assert cache_control_value(0) == "no-store"
    assert cache_control_value(-5) == "no-store"
    assert cache_control_value(60) == "public, max-age=60, s-maxage=60"
    assert cache_control_value(60, 30) == (
        "public, max-age=60, s-maxage=60, stale-while-revalidate=30"
    )


def test_svg_escapes_title_in_markup(client):
    response = client.get(
        "/28/",
        query_string={"title": "<script>alert(1)</script>"},
    )
    assert response.status_code == 200
    assert b"<script>" not in response.data
    assert b"&lt;script&gt;" in response.data


def test_dynamic_json_missing_params(client):
    response = client.get("/dynamic/json/")
    assert response.status_code == 400
    assert response.content_type == "image/svg+xml"
    assert b"missing" in response.data.lower()


def test_dynamic_json_localhost_blocked(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "http://127.0.0.1:8080/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


@patch("app.fetch_json_document")
def test_dynamic_json_query_param(mock_fetch, client):
    mock_fetch.return_value = {"v": 9}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.v",
        },
    )
    assert response.status_code == 200
    assert b"9" in response.data
    assert response.headers.get("X-Content-Type-Options") == "nosniff"


@patch("app.fetch_json_document")
def test_dynamic_json_dot_path(mock_fetch, client):
    mock_fetch.return_value = {
        "progress": [{"data": {"approvalProgress": 73}}],
    }
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/stats.json",
            "query": "progress.0.data.approvalProgress",
        },
    )
    assert response.status_code == 200
    assert response.content_type == "image/svg+xml"
    assert b"<svg" in response.data
    assert b"73" in response.data


@patch("app.fetch_json_document")
def test_dynamic_json_jsonpath_dollar(mock_fetch, client):
    mock_fetch.return_value = {"items": [{"n": 42}]}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.items[0].n",
        },
    )
    assert response.status_code == 200
    assert b"42" in response.data


@patch("app.fetch_json_document")
def test_dynamic_json_filter_expression_by_name(mock_fetch, client):
    mock_fetch.return_value = {
        "progress": [
            {"data": {"language": {"name": "Arabic"}, "translationProgress": 5}},
            {"data": {"language": {"name": "Spanish"}, "translationProgress": 87}},
        ],
    }
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/stats.json",
            "query": "$.progress[?(@.data.language.name=='Spanish')].data.translationProgress",
        },
    )
    assert response.status_code == 200
    assert b"87" in response.data


@patch("app.fetch_json_document")
def test_dynamic_json_filter_expression_no_match_returns_422(mock_fetch, client):
    mock_fetch.return_value = {
        "progress": [
            {"data": {"language": {"name": "Arabic"}, "translationProgress": 5}},
        ],
    }
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/stats.json",
            "query": "$.progress[?(@.data.language.name=='Klingon')].data.translationProgress",
        },
    )
    assert response.status_code == 422


@patch("app.fetch_json_document")
def test_dynamic_json_percent_suffix_string(mock_fetch, client):
    mock_fetch.return_value = {"approvalProgress": "73%"}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.approvalProgress",
        },
    )
    assert response.status_code == 200
    assert b"73" in response.data


@patch("app.fetch_json_document", side_effect=URLError("connection failed"))
def test_dynamic_json_fetch_failure_returns_502(mock_fetch, client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 502
    assert response.content_type == "image/svg+xml"


@patch("app.fetch_json_document")
def test_dynamic_json_query_no_match_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"other": 1}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.missing",
        },
    )
    assert response.status_code == 422
    assert response.content_type == "image/svg+xml"


@patch("app.fetch_json_document")
def test_dynamic_json_invalid_query_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"x": 1}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$$not-valid-jsonpath",
        },
    )
    assert response.status_code == 422


@patch("app.fetch_json_document")
def test_dynamic_json_boolean_value_rejected(mock_fetch, client):
    mock_fetch.return_value = {"flag": True}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.flag",
        },
    )
    assert response.status_code == 422


@patch("app.fetch_json_document")
def test_dynamic_json_cache_sets_cache_control(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
            "cache": "120",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "public, max-age=120, s-maxage=120"


@patch("app.fetch_json_document")
def test_dynamic_json_cache_seconds_alias(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
            "cacheSeconds": "60",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "public, max-age=60, s-maxage=60"


@patch("app.fetch_json_document")
def test_dynamic_json_cache_default(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={"url": "https://example.com/x.json", "query": "$.n"},
    )
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == (
        f"public, max-age={DYNAMIC_JSON_CACHE_SECONDS}, s-maxage={DYNAMIC_JSON_CACHE_SECONDS}"
    )


@patch("app.fetch_json_document")
def test_dynamic_json_cache_default_can_be_tuned(mock_fetch, client, monkeypatch):
    monkeypatch.setattr(app_module, "DYNAMIC_JSON_CACHE_SECONDS", 30)
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={"url": "https://example.com/x.json", "query": "$.n"},
    )
    assert response.headers.get("Cache-Control") == "public, max-age=30, s-maxage=30"


@patch("app.fetch_json_document")
def test_dynamic_json_cache_zero_disables_caching(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={"url": "https://example.com/x.json", "query": "$.n", "cache": "0"},
    )
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "no-store"


@patch("app.fetch_json_document")
def test_dynamic_json_cache_is_clamped(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={"url": "https://example.com/x.json", "query": "$.n", "cache": "999999"},
    )
    assert response.headers.get("Cache-Control") == (
        f"public, max-age={MAX_CACHE_SECONDS}, s-maxage={MAX_CACHE_SECONDS}"
    )


@patch("app.fetch_json_document")
def test_dynamic_json_cache_invalid_value_falls_back_to_default(mock_fetch, client):
    mock_fetch.return_value = {"n": 5}
    response = client.get(
        "/dynamic/json/",
        query_string={"url": "https://example.com/x.json", "query": "$.n", "cache": "soon"},
    )
    assert response.headers.get("Cache-Control") == (
        f"public, max-age={DYNAMIC_JSON_CACHE_SECONDS}, s-maxage={DYNAMIC_JSON_CACHE_SECONDS}"
    )


@patch("app.fetch_json_document", side_effect=URLError("connection failed"))
def test_dynamic_json_errors_are_not_cacheable(mock_fetch, client):
    response = client.get(
        "/dynamic/json/",
        query_string={"url": "https://example.com/x.json", "query": "$.x", "cache": "600"},
    )
    assert response.status_code == 502
    assert response.headers.get("Cache-Control") == "no-store"

    response = client.get("/dynamic/json/")
    assert response.status_code == 400
    assert response.headers.get("Cache-Control") == "no-store"


def test_dynamic_json_disallowed_scheme(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "ftp://example.com/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


def test_dynamic_json_url_with_userinfo_blocked(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "http://user@example.com/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


def test_dynamic_json_nonstandard_port_blocked(client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com:8080/data.json",
            "query": "$.x",
        },
    )
    assert response.status_code == 400


def test_dynamic_json_url_too_long_blocked(client):
    pad_len = JSON_URL_MAX_LENGTH - len("https://example.com/") + 10
    long_url = "https://example.com/" + ("x" * max(1, pad_len))
    assert len(long_url) > JSON_URL_MAX_LENGTH
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": long_url,
            "query": "$.x",
        },
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    "metadata_url",
    [
        "http://169.254.169.254/latest/meta-data",
        "http://metadata.google.internal/computeMetadata/v1",
    ],
)
def test_dynamic_json_cloud_metadata_hosts_blocked(client, metadata_url):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": metadata_url,
            "query": "$.x",
        },
    )
    assert response.status_code == 400


@patch("app.fetch_json_document")
def test_dynamic_json_matched_string_empty_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"s": "   "}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.s",
        },
    )
    assert response.status_code == 422
    assert b"empty" in response.data.lower()


@patch("app.fetch_json_document")
def test_dynamic_json_matched_string_not_numeric_returns_422(mock_fetch, client):
    mock_fetch.return_value = {"s": "foo"}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.s",
        },
    )
    assert response.status_code == 422
    assert b"numeric" in response.data.lower()


@patch("app._fetch_json_opener.open", side_effect=URLError("http redirect not allowed"))
def test_dynamic_json_http_redirect_from_server_is_blocked(mock_open, client):
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 502


@patch("app._fetch_json_opener.open")
def test_dynamic_json_malformed_json_body_returns_422(mock_open, client):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b'{"n": }'
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 422


@patch("app._fetch_json_opener.open")
def test_dynamic_json_invalid_utf8_body_returns_422(mock_open, client):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=utf-8"
    mock_resp.read.return_value = b"\xff"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 422


@patch("app._fetch_json_opener.open")
def test_dynamic_json_response_too_large_returns_422(mock_open, client):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b"x" * (JSON_FETCH_MAX_BYTES + 1)
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/x.json",
            "query": "$.n",
        },
    )
    assert response.status_code == 422
    assert b"large" in response.data.lower()


@patch("app._fetch_json_opener.open")
def test_fetch_json_rejects_html_content_type(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "text/html; charset=utf-8"
    mock_resp.read.return_value = b"{}"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(ValueError, match="unsupported content type"):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_allows_application_json(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=utf-8"
    mock_resp.read.return_value = b'{"n": 3}'
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    assert fetch_json_document("https://example.com/x.json") == {"n": 3}


@patch("app._fetch_json_opener.open")
def test_fetch_json_respects_charset_iso8859_1(mock_open):
    payload = '{"a": "caf\xe9"}'
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=iso-8859-1"
    mock_resp.read.return_value = payload.encode("iso-8859-1")
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    assert fetch_json_document("https://example.com/x.json") == {"a": "café"}


@patch("app._fetch_json_opener.open")
def test_fetch_json_unsupported_charset_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=x-unknown-xyz"
    mock_resp.read.return_value = b"{}"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(ValueError, match="unsupported charset"):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_response_too_large_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b"x" * (JSON_FETCH_MAX_BYTES + 1)
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(ValueError, match="response too large"):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_invalid_utf8_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json; charset=utf-8"
    mock_resp.read.return_value = b"\xff"
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(UnicodeDecodeError):
        fetch_json_document("https://example.com/x.json")


@patch("app._fetch_json_opener.open")
def test_fetch_json_malformed_json_raises(mock_open):
    mock_resp = MagicMock()
    mock_resp.headers.get.return_value = "application/json"
    mock_resp.read.return_value = b'{"n": }'
    ctx = MagicMock()
    ctx.__enter__.return_value = mock_resp
    ctx.__exit__.return_value = None
    mock_open.return_value = ctx
    with pytest.raises(json.JSONDecodeError):
        fetch_json_document("https://example.com/x.json")


# --- Negative values and fill origin (issue #64) -------------------------------

FILL_RECT = re.compile(
    rb'Progress fill.*?<rect rx="[^"]*" x="([^"]+)" width="([^"]+)" height="100%" fill="#([0-9a-fA-F]+)"',
    re.DOTALL,
)


def _fill(response):
    """Return (x, width, color) of the progress fill rect."""
    match = FILL_RECT.search(response.data)
    assert match, response.data
    return float(match.group(1)), float(match.group(2)), match.group(3).decode()


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, "left"),
        ("", "left"),
        ("left", "left"),
        ("center", "center"),
        ("middle", "center"),
        ("Centre", "center"),
        ("right", "right"),
        ("bogus", "left"),
    ],
)
def test_parse_progress_origin(value, expected):
    assert parse_progress_origin(value) == expected


@pytest.mark.parametrize(
    "progress, origin, expected",
    [
        (50, "left", (0, 50)),
        (-50, "left", (0, 50)),
        (150, "left", (0, 100)),
        (50, "right", (50, 50)),
        (-25, "right", (75, 25)),
        (0, "center", (50, 0)),
        (50, "center", (50, 25)),
        (-50, "center", (25, 25)),
        (100, "center", (50, 50)),
        (-100, "center", (0, 50)),
        (-500, "center", (0, 50)),
    ],
)
def test_get_fill_geometry(progress, origin, expected):
    assert get_fill_geometry(progress, 100, 100, 0, origin) == expected


def test_get_fill_geometry_offsets_by_title_width():
    assert get_fill_geometry(-50, 100, 100, 40, "center") == (65, 25)
    assert get_fill_geometry(50, 100, 100, 40, "center") == (90, 25)


def test_negative_value_route_is_accepted(client):
    response = client.get("/-28/")
    assert response.status_code == 200
    assert response.content_type == "image/svg+xml"
    assert b"-28%" in response.data


def test_negative_value_default_origin_fills_absolute_value(client):
    response = client.get("/-50/", query_string={"width": "100"})
    x, width, _ = _fill(response)
    assert (x, width) == (0, 50)


def test_center_origin_positive_grows_right(client):
    response = client.get("/50/", query_string={"width": "100", "origin": "center"})
    x, width, _ = _fill(response)
    assert (x, width) == (50, 25)
    assert b"Zero axis" in response.data


def test_center_origin_negative_grows_left(client):
    response = client.get("/-50/", query_string={"width": "100", "origin": "center"})
    x, width, color = _fill(response)
    assert (x, width) == (25, 25)
    assert color == "d9534f"


def test_center_origin_with_title(client):
    response = client.get(
        "/-100/", query_string={"width": "100", "origin": "middle", "title": "delta"}
    )
    title_width = 10 + 6 * len("delta")
    x, width, _ = _fill(response)
    assert (x, width) == (title_width, 50)


def test_right_origin_grows_from_right(client):
    response = client.get("/25/", query_string={"width": "100", "origin": "right"})
    x, width, _ = _fill(response)
    assert (x, width) == (75, 25)
    assert b"Zero axis" not in response.data


def test_negative_color_applies_only_to_negative_values(client):
    query = {"origin": "center", "negative_color": "ff0000", "progress_color": "00ff00"}
    _, _, negative = _fill(client.get("/-10/", query_string=query))
    _, _, positive = _fill(client.get("/10/", query_string=query))
    assert negative == "ff0000"
    assert positive == "00ff00"


def test_non_positive_scale_falls_back_to_default(client):
    for scale in ("0", "-10"):
        response = client.get("/50/", query_string={"scale": scale, "width": "100"})
        assert response.status_code == 200
        _, width, _ = _fill(response)
        assert width == 50


@patch("app.fetch_json_document")
def test_dynamic_json_negative_value_center_origin(mock_fetch, client):
    mock_fetch.return_value = {"delta": -40}
    response = client.get(
        "/dynamic/json/",
        query_string={
            "url": "https://example.com/data.json",
            "query": "delta",
            "origin": "center",
            "width": "100",
        },
    )
    assert response.status_code == 200
    x, width, _ = _fill(response)
    assert (x, width) == (30, 20)
