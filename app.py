from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

def is_true(value):
  return value.lower() == 'true'

def get_progress_color(progress, scale):
    """Get the color representation of progress based on a scale.

    This function calculates the ratio of progress to scale and returns a
    color code that represents the level of progress. The color codes are
    defined as follows: - Red ("d9534f") for progress less than 30% - Yellow
    ("f0ad4e") for progress between 30% and 70% - Green ("5cb85c") for
    progress of 70% or more.

    If scale is 0, the function returns "d9534f"(red) by default to indicate no progress and avoid a zero division error.

    Args:
        progress (float): The current progress value.
        scale (float): The maximum scale value to compare against.

    Returns:
        str: A hex color code representing the progress level.
    """
    if scale == 0:
        return "d9534f" # Default to red if scale is 0 (avoiding division by zero)
    
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

    # Handles case sensitivity
    style = style.lower()

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
        "thin-rounded": {
            "border_radius": 10,  # Fully rounded corners
            "progress_width": 40,  # Thinner progress bar
            "height": 10,  # Reduced height for a sleek look
            "progress_color": "4CAF50",  # Soft green
            "progress_background": "DDD",  # Light gray background
            "title_color": "333",  # Darker title text for contrast
            "font_size": 10,  # Smaller font for balance
            "show_shadow": False,
        },
        "neo-glass": {
            "border_radius": 6,
            "progress_width": 60,
            "height": 18,
            "progress_color": "6a11cb",  # Gradient effect (purple-blue)
            "progress_background": "2575fc",
            "title_color": "fff",
            "font_size": 12,
            "show_shadow": True,
            "gradient": True,  # Enables smooth gradient blending
        },
        "minimal-matte": {
            "border_radius": 2,  # Subtle rounding
            "progress_width": 50,
            "height": 14,
            "progress_color": "333",  # Dark gray for a matte feel
            "progress_background": "EEE",  # Light gray background
            "title_color": "000",  # Black title for high contrast
            "font_size": 11,
            "letter_spacing": 1,
            "show_shadow": False,  # Completely flat design
        }
    }
    return style_templates.get(style, {})

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

    scale = 100 # Default scale

    try:
        scale = int(request.args.get("scale", 100)) # Default to 100 if missing
        if scale < 1:
            raise ValueError
    except (TypeError, ValueError):
        scale = 100

    if request.args.get("as_percent"):
        progress_text = f"{int(progress / scale * 100)}%" # Format as percentage



    progress_width = 60 if title else 90 # Default values

    try:
        progress_width = int(request.args.get("width"))

        if title and not (10 <= progress_width <= 100): # Ensure valid range
                raise ValueError
        if not title and not (90 <= progress_width <= 300): # Ensure valid range
                raise ValueError
        
    except (TypeError, ValueError):
        progress_width = 60 if title else 90  # Reset to default on error


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
