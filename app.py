from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

def get_progress_color(progress, scale):
    ratio = progress/scale

    if ratio < 0.3:
        return "d9534f"
    if ratio < 0.7:
        return "f0ad4e"

    return "5cb85c"


def get_template_fields(progress):
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
