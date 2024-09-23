from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

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

    scale = 100
    try:
        scale = int(request.args.get("scale"))
    except (TypeError, ValueError):
        pass

    progress_width = 60 if title else 90
    try:
        progress_width = int(request.args.get("width"))
    except (TypeError, ValueError):
        pass

    return {
        "title": title,
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": request.args.get("color", "428bca"),
        "scale": scale,
        "progress": progress,
        "progress_width": progress_width,
        "progress_color": request.args.get("progress_color", get_progress_color(progress, scale)),
        "progress_background": request.args.get("progress_background", "555"),
        "progress_number_color": request.args.get("progress_number_color", "fff"),
        "prefix": request.args.get("prefix", ""),
        "suffix": request.args.get("suffix", "%"),
        "show_text": request.args.get("show_text", "true"),
    }

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
