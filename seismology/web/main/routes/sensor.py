from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
import requests, json

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")

@sensor.route("/")
@register_breadcrumb(sensor,".",'Sensors')
def index():
    r = requests.get(current_app.config["API_URL"]+"/sensors",headers={"content-type":"application"}, json={})
    print("este es el error---->", r)
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
