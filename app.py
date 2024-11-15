from flask import Flask, make_response, redirect, render_template, request
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/progress')
def progress():
    return render_template('progress.html')


def is_true(value):

    app.add_url_rule('/progress', 'progress', progress)
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
            #
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
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": request.args.get("color"),
        "scale": scale,
        "progress": progress,
        "progress_text": progress_text,
        "progress_width": progress_width,
        "progress_color": request.args.get("progress_color"),
        "negative_progress_color": request.args.get("negative_progress_color"),
        "progress_background": request.args.get("progress_background"),
        "progress_number_color": request.args.get("progress_number_color"),
        "prefix": request.args.get("prefix"),
        "suffix": request.args.get("suffix"),
        "show_text": show_text,
        "show_shadow": show_shadow,
        "border_radius": request.args.get("radius"),
    }

    default = get_style_fields("default")
    style = get_style_fields(request.args.get("style"))
    clean_req_params = {k: v for k, v in req_params.items() if v is not None}

    if "progress_color" not in clean_req_params:

    if "negative_progress_color" not in clean_req_params:
        clean_req_params["negative_progress_color"] = "ff0000"  # Default red for negative values
        clean_req_params["progress_color"] = style.get("progress_color") or default.get("progress_color", get_progress_color(progress, scale))

    return {**default, **style, **clean_req_params}

@app.route("/<int:progress>/")
def get_progress_svg(progress):
    template_fields = get_template_fields(progress)

    template = render_template("progress.svg", **template_fields)

    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response

@app.route("/")
def redirect_to_github():
    return redirect("https://github.com/guibranco/progressbar", code=302)

if __name__ == "__main__":
    app.run()
