from flask import Blueprint, redirect, url_for
from flask_breadcrumbs import register_breadcrumb


home = Blueprint("home", __name__, url_prefix="/")

@home.route("/")
@register_breadcrumb(home, 'breadcrumbs.', 'Home')
def index():
    return redirect(url_for("main.index"))


