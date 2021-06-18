import logging
from os import getenv

import jinja2

from progress import get_progress_color

logging.basicConfig(
    format="%(asctime)s %(message)s", level=getenv("LOG_LEVEL", "DEBUG")
)
LOGGER = logging.getLogger(__name__)


def render_template(template_name, **template_vars):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
    template = env.get_template(template_name)
    return template.render(**template_vars)


def redirect_to_github():
    return {
        "statusCode": 301,
        "headers": {
            "Content-Type": "text/html",
            "Location": "https://github.com/fredericojordan/progress-bar",
        },
        "isBase64Encoded": False,
    }


def lambda_handler(event, context):
    LOGGER.debug({"event": event, "context": context})

    try:
        return render_svg(event, int(event["pathParameters"]["progress"]))
    except (TypeError, ValueError):
        return redirect_to_github()


def render_svg(event, progress):
    query_params = event.get("queryStringParameters", {})

    title = query_params.get("title")
    try:
        scale = int(query_params.get("scale"))
    except (TypeError, ValueError):
        scale = 100

    try:
        progress_width = int(query_params.get("width"))
    except (TypeError, ValueError):
        progress_width = 60 if title else 90

    template_fields = {
        "title": title,
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": query_params.get("color", "428bca"),
        "scale": scale,
        "progress": progress,
        "progress_width": progress_width,
        "progress_color": get_progress_color(progress, scale),
        "suffix": query_params.get("suffix", "%"),
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "image/svg+xml"},
        "body": render_template("progress.svg", **template_fields),
        "isBase64Encoded": False,
    }
