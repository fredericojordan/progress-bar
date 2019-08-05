from flask import Flask, render_template

app = Flask(__name__)


@app.route("/<int:progress>/")
def getProgressSVG(progress):
    color = "#5cb85c"
    if progress < 70:
        color = "#f0ad4e"
    if progress < 30:
        color = "#d9534f"

    return render_template("progress.svg", width=90, progress=progress, color=color)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
