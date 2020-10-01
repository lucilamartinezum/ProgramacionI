from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from ..forms.user_form import UserForm, UserEdit
from ..utilities.functions import sendRequest
from .auth import admin_required

from flask_login import login_required

import requests, json

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/")
@login_required
@admin_required
@register_breadcrumb(user, '.', 'Users')
def index():
    req = sendRequest(method="get", url="/users", auth=True)
    users = json.loads(req.text)['Users']
    title = "Users List"
    return render_template("users.html", title=title, users=users) # Mostrar template

@user.route("/add-user", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(user, ".add", "Add User")
def create():
    form = UserForm() # Instanciar formulario
    if form.validate_on_submit(): # Si el formulario ha sido enviado y es valido correctamente
        user = {
            "email": form.email.data,
            "password": form.password.data,
            "admin": form.admin.data
        }
        data = json.dumps(user)
        req = sendRequest(method="post", url="/users", data=data, auth=True)
        return redirect(url_for("user.index")) # Redirecciona a la lista de usuarios
    return render_template("user_form.html", form=form)

@user.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
@admin_required
@register_breadcrumb(user, ".edit", "Edit User")
def edit(id):
    form = UserEdit()
    if not form.is_submitted():
        req = sendRequest(method="get", url="/user/" + str(id), auth=True)
        if (req.status_code == 404):
            flash("User not found","danger")
            return redirect(url_for("user.index"))
        user = json.loads(req.text)
        form.email.data = user["email"]
        form.admin.data = user["admin"]

    if form.validate_on_submit():
        user = {
            "email": form.email.data,
            "admin": form.admin.data
        }
        data = json.dumps(user)
        req = sendRequest(method="put", url="/user/" + str(id), data=data, auth=True)
        flash("User has been edited","success")
        return redirect(url_for("user.index"))
    return render_template("user-edit.html", form=form, id=id)


@user.route('delete/<int:id>')
@login_required
@admin_required
def delete(id):
    req = sendRequest(method="delete", url="/user/" + str(id), auth=True)
    flash("User has been deleted", "danger")
    return redirect(url_for('user.index'))


