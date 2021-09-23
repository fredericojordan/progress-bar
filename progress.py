import os

from flask import Flask, make_response, redirect, render_template, request, send_from_directory

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "secret_l801#+#a&^1mz)_p&qyq51j51@20_74c-xi%&i)b*u_dt^2=2key"
)


def get_progress_color(progress, scale):
    ratio = progress / scale

    if ratio < 0.3:
        return "#d9534f"
    if ratio < 0.7:
        return "#f0ad4e"

    return "#5cb85c"


def get_template_fields(progress):
    padding = 8
    chinese_char_width = 11.167 # DejaVu Sans Mono
    english_char_width = 6.628

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

    def title_width(title):
        width = 0
        for _char in title:
            if '\u4e00' <= _char <= '\u9fa5':
                width += chinese_char_width
            else:
                width += english_char_width
        return padding + width

    return {
        "title": title,
        "title_width": title_width(title) if title else 0,
        "title_color": request.args.get("color", "428bca"),
        "scale": scale,
        "progress": progress,
        "progress_width": progress_width,
        "progress_color": get_progress_color(progress, scale),
        "suffix": request.args.get("suffix", "%"),
    }


@app.route("/<int:progress>/")
def get_progress_svg(progress):
    template_fields = get_template_fields(progress)

    template = render_template("progress.svg", **template_fields)

    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response

@app.route("/fonts/<filename>")
def download(filename):
    return send_from_directory(directory="fonts", filename=filename)

@app.route("/")
def redirect_to_github():
    return redirect("https://github.com/tuchengpanghu/progress-bar", code=302)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
