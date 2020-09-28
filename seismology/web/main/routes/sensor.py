from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
import requests, json

from ..forms.sensor import SensorForm, SensorEdit

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")

@sensor.route("/")
@register_breadcrumb(sensor,".",'Sensors')
def index():
    r = requests.get(current_app.config["API_URL"]+"/sensors",headers={"content-type":"application"}, json={})
    sensors = json.loads(r.text)['Sensors']
    title = "Sensors"
    return render_template("sensors.html",title=title,sensors=sensors)

@sensor.route("/view/<int:id>")
@register_breadcrumb(sensor, '.view', 'View')
def view(id):
    r = requests.get(current_app.config["API_URL"]+"/sensor/"+str(id),headers={"content-type":"application/json"})
    if (r.status_code == 404):
        return redirect(url_for("sensor.index"))
    sensor = json.loads(r.text)
    title = "Sensor View"
    return render_template("sensor-view.html", title=title, sensor=sensor)

@sensor.route("/add-sensor", methods=["GET", "POST"])
@register_breadcrumb(sensor, ".add", "Add Sensor")
def create():
    form = SensorForm()# Instanciar formulario
    r = requests.get(current_app.config["API_URL"]+"/users", headers={"content-type":"application/json"})
    form.userId.choices=[(int(user["id"]), user["email"]) for user in json.loads(r.text)["Users"]]
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
        print(data)
        r = requests.post(current_app.config["API_URL"]+"/sensors",headers={"content-type":"application/json"}, data=data)
        print(r)
        return redirect(url_for("sensor.index")) # Redirecciona a la lista de usuarios
    return render_template("add-sensor.html", form=form)

@sensor.route("/edit/<int:id>", methods=["GET","POST"])
@register_breadcrumb(sensor, ".edit", "Edit Sensor")
def edit(id):
    form = SensorEdit()
    r = requests.get(current_app.config["API_URL"] + "/users", headers={"content-type": "application/json"})
    form.userId.choices = [(int(user["id"]), user["email"]) for user in json.loads(r.text)["Users"]]
    form.userId.choices.insert(0, [0, "Select one User"])
    url = current_app.config["API_URL"]+"/sensor/"+str(id)
    if not form.is_submitted():
        r = requests.get(url, headers={"content-type":"application/json"})
        #r = sendRequest(method="get", url="/sensor/" + str(id), auth=True)
        if (r.status_code == 404):
            flash("Sensor not found","danger")
            return redirect(url_for("sensor.index"))
        sensor = json.loads(r.text)
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
        r = requests.put(url, headers={"content-type":"application/json"}, data=data)
        flash("Sensor has been edited","success")
        return redirect(url_for("sensor.index"))
    return render_template("edit-sensor.html", form=form, id=id)


@sensor.route('delete/<int:id>')
def delete(id):
    url = current_app.config["API_URL"] + "/sensor/" + str(id)
    requests.delete(url, headers={'content-type': 'application/json'})
    #r = sendRequest(method="delete", url="/user/" + str(id), auth=True)
    flash("Sensor has been deleted", "danger")
    return redirect(url_for('sensor.index'))