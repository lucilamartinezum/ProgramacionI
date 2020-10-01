from flask import Blueprint, render_template, current_app, redirect, url_for, flash
import requests, json
from flask_breadcrumbs import register_breadcrumb
from ..utilities.functions import sendRequest
from ..forms.unverified_seism import UnverifiedSeismEdit
from flask_login import login_required

unverified_seism = Blueprint("unverified_seism", __name__, url_prefix="/unverified-seism")

@unverified_seism.route("/")
@login_required
@register_breadcrumb(unverified_seism, '.', 'Unverified Seisms')
def index():
    req = sendRequest(method="get", url="/unverified-seisms", auth=True)
    unverified_seisms = json.loads(req.text)["Unverified-Seisms"]
    title = "Unverified Seisms List"
    return render_template("unverified-seisms.html", title=title, unverified_seisms=unverified_seisms)

@unverified_seism.route("/view/<int:id>")
@login_required
@register_breadcrumb(unverified_seism, '.view', 'View')
def view(id):
    req = sendRequest(method="get", url="/unverified-seism/" + str(id), auth=True)
    if (req.status_code == 404):
        flash("Seism not found", "danger")
        return redirect(url_for("unverified_seism.index"))
    unverified_seism = json.loads(req.text)
    title = "Unverified Seism View"
    return render_template("unverified_seism.html", title=title, unverified_seism=unverified_seism)

@unverified_seism.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
@register_breadcrumb(unverified_seism, ".edit", "Edit Unverified Seism")
def edit(id):
    form = UnverifiedSeismEdit()
    if not form.is_submitted():
        req = sendRequest(method="get", url="/unverified-seism/" + str(id), auth=True)
        if (req.status_code == 404):
            flash("Unverified Seism not found","danger")
            return redirect(url_for("unverified_seism.index"))
        unverified_seism = json.loads(req.text)
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
        req = sendRequest(method="put", url="/unverified-seism/" + str(id), data=data, auth=True)
        flash("Unverified Seism has been edited","success")
        return redirect(url_for("unverified_seism.index"))
    return render_template("edit-unverifiedseism.html", form=form, id=id)

@unverified_seism.route('delete/<int:id>')
@login_required
def delete(id):
    req = sendRequest(method="delete", url="/unverified-seism/" + str(id), auth=True)
    flash("Unverified Seism has been deleted", "danger")
    return redirect(url_for('unverified_seism.index'))

