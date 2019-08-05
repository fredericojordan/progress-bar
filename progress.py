import os

from flask import Flask, make_response, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret_l801#+#a&^1mz)_p&qyq51j51@20_74c-xi%&i)b*u_dt^2=2key")


@app.route("/<int:progress>/")
def getProgressSVG(progress):
    color = "#5cb85c"
    if progress < 70:
        color = "#f0ad4e"
    if progress < 30:
        color = "#d9534f"

    template = render_template("progress.svg", width=90, progress=progress, color=color)
    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
