from flask import Blueprint, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
from . import unverified_seism
from . import verified_seism

home = Blueprint("home", __name__, url_prefix="/")

@home.route("/")
@register_breadcrumb(home, 'breadcrumbs.', 'Home')
def index():
    return redirect(url_for("verified_seism.index"))


