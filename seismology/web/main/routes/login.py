import json

from flask import Blueprint, current_app, flash, make_response, redirect, url_for, render_template
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_user, logout_user
import requests

from ..forms.login import LoginForm
from .auth import User

log = Blueprint("login", __name__, url_prefix="/")


@log.route("/login", methods=["POST","GET"])
@register_breadcrumb(log,".",'login')
def login():
    url = current_app.config['API_URL'] + '/auth/login'
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        # Enviar requests
        data = '{"email":"' + loginForm.email.data + \
            '", "password":"' + loginForm.password.data + '"}'
        r = requests.post(
            current_app.config["API_URL"]+"/auth/login",
            headers={"content-type": "application/json"},
            data=data
        )
        # Si la request se realiza con exito
        if r.status_code == 200:
            # Cargar valores del usuario de la respuesta
            user_data = json.loads(r.text)
            user = User(id=user_data.get("id"), email=user_data.get(
                "email"), admin=user_data.get("admin"))
            # Loguear objeto usuario
            login_user(user)
            # Crear una request de redireccion
            req = make_response(redirect(url_for("main.index")))
            # Setear cookie con el valor del token
            req.set_cookie("access_token", user_data.get(
                "access_token"), httponly=True)
            # Realizar la request
            return req

        else:
            # Mostrar error de autenticacion
            flash("Incorrect user or password", "danger")

    return render_template("login.html", loginForm=loginForm)


@log.route("/logout")
def logout():
    # Crear una request de redireccion
    req = make_response(redirect(url_for("main.index")))
    # Vaciar cookie
    req.set_cookie("access_token", "", httponly=True)
    # Desloguear usuario
    logout_user()
    # Realizar request
    return req