from flask import Blueprint, render_template, current_app, redirect, url_for, flash
import requests, json
from flask_breadcrumbs import register_breadcrumb
from ..utilities.functions import sendRequest

verified_seism = Blueprint("verified_seism", __name__, url_prefix="/verified-seism")

@verified_seism.route("/")
@register_breadcrumb(verified_seism, '.', 'Verified Seisms')
def index():
    req = sendRequest(method="get", url="/verified-seisms", )
    verified_seisms = json.loads(req.text)['Verified-Seism']
    data = {}
    title = "Verified Seisms List"
    return render_template("verified-seisms.html", title=title, verified_seisms=verified_seisms)

@verified_seism.route("/view/<int:id>")
@register_breadcrumb(verified_seism, '.view', 'View')
def view(id):
    req = sendRequest(method="get", url="/verified-seism/" + str(id), )
    if (req.status_code == 404):
        return redirect(url_for("verified_seism.index"))
    verified_seism = json.loads(req.text)
    title = "Verified Seism View"
    return render_template("verified-seism.html", title=title, verified_seism=verified_seism)

@verified_seism.route('delete/<int:id>')
def delete(id):
    req = sendRequest(method="delete", url="/verified-seism/" + str(id), auth=True)
    flash("Verified Seism has been deleted", "danger")
    return redirect(url_for('verified_seism.index'))

