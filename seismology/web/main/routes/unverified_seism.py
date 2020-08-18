from flask import Blueprint, render_template, current_app, redirect, url_for
import requests, json
from flask_breadcrumbs import register_breadcrumb

unverified_seism = Blueprint("unverified_seism", __name__, url_prefix="/unverified-seism")

@unverified_seism.route("/")
@register_breadcrumb(unverified_seism, '.', 'Unverified Seisms')
def index():
    r = requests.get(current_app.config["API_URL"]+"/unverified-seisms",headers={"content-type":"application/json"})
    unverified_seisms = json.loads(r.text)["Unverified-Seisms"]
    title = "Unverified Seisms List"
    return render_template("unverified-seisms.html", title=title, unverified_seisms=unverified_seisms)

@unverified_seism.route("/view/<int:id>")
@register_breadcrumb(unverified_seism, '.view', 'View')
def view(id):
    r = requests.get(current_app.config["API_URL"]+"/unverified-seism/"+str(id),headers={"content-type":"application/json"})
    if (r.status_code == 404):
        return redirect(url_for("unverified_seism.index"))
    unverified_seism = json.loads(r.text)
    title = "Unverified Seism View"
    return render_template("unverified_seism.html", title=title, unverified_seism=unverified_seism)
