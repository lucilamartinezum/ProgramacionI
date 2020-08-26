from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from ..forms.user_form import UserForm
import requests, json

user = Blueprint("user", __name__, url_prefix="/user")
# default_breadcrumb_root(user, ".main")

@user.route("/")
@register_breadcrumb(user, '.', 'Users')
def index():
    r = requests.get(current_app.config["API_URL"]+"/users",headers={"content-type":"application/json"})
    users = json.loads(r.text)['Users']
    title = "Users List"
    return render_template("users.html", title=title, users=users) # Mostrar template

@user.route("/add-user", methods=["GET", "POST"])
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
        print(data)
        r = requests.post(current_app.config["API_URL"]+"/users",headers={"content-type":"application/json"}, data=data)
        print(r)
        return redirect(url_for("user.index")) # Redirecciona a la lista
    return render_template("user_form.html", form=form)

@user.route("/edit-user", methods=["GET", "POST"])
def edit():
    form = UserEdit()
    url = current_app.config["API_URL"] + "/user/" + str(id)
    if not form.is_submitted():
        r = requests.get(url=url, headers={'content-type':"application/json"})
        if r.status_code == 404:
            return redirect(url_for("user.index"))
        user = r.json()
        print(user)
        form.email.r = user["email"]
        if user["admin"] == False:
            form.admin.r = "false"
        else:
            form.admin.r ="true"

    if form.validate_on_submit():
        if form.admin.r == "false":
            form.admin.r = False
        else:
            form.admin.r = True
        user = {
            "email": form.email.r,
            "admin": form.admin.r
        }
        user_json = json.dumps(user)
        r = requests.put(url=url, headers={"content-type": "application/json"}, r=user_json)
        return redirect(url_for("user.index"))
    return render_template("user-edit.html", id=id, form=form)


