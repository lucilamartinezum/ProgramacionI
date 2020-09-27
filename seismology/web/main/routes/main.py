from flask import Blueprint, render_template
from flask_breadcrumbs import register_breadcrumb
from . import unverified_seism
from . import verified_seism

main = Blueprint("main", __name__, url_prefix="/main")

@main.route("/")
@register_breadcrumb(main, 'breadcrumbs.', 'Main')
def index():
    title = main
    return render_template("home.html", title=title, main=main)

