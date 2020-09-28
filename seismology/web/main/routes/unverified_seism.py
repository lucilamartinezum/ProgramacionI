from flask import Blueprint, render_template, current_app, redirect, url_for, flash
import requests, json
from flask_breadcrumbs import register_breadcrumb
from ..forms.unverified_seism import UnverifiedSeismEdit

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

@unverified_seism.route("/edit/<int:id>", methods=["GET","POST"])
@register_breadcrumb(unverified_seism, ".edit", "Edit Unverified Seism")
def edit(id):
    form = UnverifiedSeismEdit()
    url = current_app.config["API_URL"]+"/unverified-seism/"+str(id)
    if not form.is_submitted():
        r = requests.get(url, headers={"content-type":"application/json"})
        #r = sendRequest(method="get", url="/user/" + str(id), auth=True)
        if (r.status_code == 404):
            flash("Unverified Seism not found","danger")
            return redirect(url_for("unverified_seism.index"))
        unverified_seism = json.loads(r.text)
        form.depth.data = unverified_seism["depth"]
        form.magnitude.data = unverified_seism["magnitude"]
        form.verified.data = unverified_seism["verified"]

    if form.validate_on_submit():
        unverified_seism = {
            "depth": form.depth.data,
            "magnitude": form.magnitude.data,
            "verified": form.verified.data,
        }
        data = json.dumps(unverified_seism)
        r = requests.put(url, headers={"content-type":"application/json"}, data=data)
        flash("Unverified Seism has been edited","success")
        return redirect(url_for("unverified_seism.index"))
    return render_template("edit-unverifiedseism.html", form=form, id=id)

@unverified_seism.route('delete/<int:id>')
def delete(id):
    url = current_app.config["API_URL"] + "/unverified-seism/" + str(id)
    requests.delete(url, headers={'content-type': 'application/json'})
    #r = sendRequest(method="delete", url="/user/" + str(id), auth=True)
    flash("Unverified Seism has been deleted", "danger")
    return redirect(url_for('unverified_seism.index'))

