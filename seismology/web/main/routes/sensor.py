from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
import requests, json

from ..forms.sensor import SensorForm, SensorEdit
from ..utilities.functions import sendRequest
from .auth import admin_required
from flask_login import login_required

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")

@sensor.route("/")
@login_required
@admin_required
@register_breadcrumb(sensor,".",'Sensors')
def index():
    req = sendRequest(method="get", url="/sensors", auth=True)
    sensors = json.loads(req.text)['Sensors']
    title = "Sensors"
    return render_template("sensors.html",title=title,sensors=sensors)

@sensor.route("/view/<int:id>")
@login_required
@admin_required
@register_breadcrumb(sensor, '.view', 'View')
def view(id):
    req = sendRequest(method="get", url="/sensor/" + str(id), auth=True)
    if (req.status_code == 404):
        flash("Sensor not found", "danger")
        return redirect(url_for("sensor.index"))
    sensor = json.loads(req.text)
    title = "Sensor View"
    return render_template("sensor-view.html", title=title, sensor=sensor)

@sensor.route("/add-sensor", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".add", "Add Sensor")
def create():
    form = SensorForm()# Instanciar formulario
    req = sendRequest(method="get", url="/users", auth=True)
    form.userId.choices=[(int(user["id"]), user["email"]) for user in json.loads(req.text)["Users"]]
    form.userId.choices.insert(0,[0, "Select one User"])
    if form.validate_on_submit(): # Si el formulario ha sido enviado y es valido correctamente
        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.userId.data,
        }
        data = json.dumps(sensor)
        req = sendRequest(method="post", url="/sensors", data=data, auth=True)

        return redirect(url_for("sensor.index")) # Redirecciona a la lista de sensores
    return render_template("add-sensor.html", form=form)

@sensor.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".edit", "Edit Sensor")
def edit(id):
    form = SensorEdit()
    req = sendRequest(method="get", url="/users", auth=True)
    form.userId.choices = [(int(user["id"]), user["email"]) for user in json.loads(req.text)["Users"]]
    form.userId.choices.insert(0, [0, "Select one User"])
    if not form.is_submitted():
        req = sendRequest(method="get", url="/sensor/" + str(id), auth=True)
        if (req.status_code == 404):
            flash("Sensor not found","danger")
            return redirect(url_for("sensor.index"))
        sensor = json.loads(req.text)
        # cargar datos
        form.name.data = sensor["name"]
        form.ip.data = sensor["ip"]
        form.port.data = sensor["port"]
        form.status.data = sensor["status"]
        form.active.data = sensor["active"]

    if form.validate_on_submit():
        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.userId.data
        }
        data = json.dumps(sensor)
        req = sendRequest(method="put", url="/sensor/" + str(id), data=data, auth=True)
        flash("Sensor has been edited","success")
        return redirect(url_for("sensor.index"))
    return render_template("edit-sensor.html", form=form, id=id)


@sensor.route('delete/<int:id>')
@login_required
@admin_required
def delete(id):
    req = sendRequest(method="delete", url="/sensor/" + str(id), auth=True)
    flash("Sensor has been deleted", "danger")
    return redirect(url_for('sensor.index'))