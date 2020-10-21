from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
import requests, json
from flask_breadcrumbs import register_breadcrumb
from ..utilities.functions import sendRequest
from ..forms.verified_seism import VerifiedSeismsFilter
import io, csv
from flask import make_response

verified_seism = Blueprint("verified_seism", __name__, url_prefix="/verified-seism")

@verified_seism.route("/")
@register_breadcrumb(verified_seism, '.', 'Verified Seisms')
def index():
    filter = VerifiedSeismsFilter(request.args, meta={"csrf": False})
    req = sendRequest(method="get", url="/sensors-info", auth=True)
    filter.sensorId.choices = [(int(sensor["id"]), sensor["name"]) for sensor in json.loads(req.text)["Sensors"]]
    filter.sensorId.choices.insert(0, [0, "All"])
    data = {}

    # Aplicado de filtros
    # Validar formulario de filtro
    if filter.validate():
        if filter.sensorId.data != None and filter.sensorId.data != 0:
            data["sensorId"] = filter.sensorId.data
        # Datetime
        if filter.from_datetime.data and filter.to_datetime.data:
            if filter.from_datetime.data == filter.to_datetime.data:
                data["datetime"] = filter.to_datetime.data.strftime('%Y-%m-%d %H:%M')
        if filter.from_datetime.data != None:
            data["from_date"] = filter.from_datetime.data.strftime('%Y-%m-%d %H:%M')
        if filter.to_datetime.data != None:
            data["to_date"] = filter.to_datetime.data.strftime('%Y-%m-%d %H:%M')




        # Depth
        if filter.depth_min.data and filter.depth_max.data:
            if filter.depth_min.data == filter.depth_max.data:
                data["depth"] = filter.depth_max.data
        if filter.depth_min.data != None:
            data["depth_min"] = filter.depth_min.data
        if filter.depth_max.data != None:
            data["depth_max"] = filter.depth_max.data

        # Magnitude
        if filter.magnitude_min.data and filter.magnitude_max:
            if filter.magnitude_min.data == filter.magnitude_max.data:
                data["magnitude"] = filter.magnitude_max.data
        if filter.magnitude_min.data != None:
            data["magnitude_min"] = filter.magnitude_min.data
        if filter.magnitude_max.data != None:
            data["magnitude_max"] = filter.magnitude_max.data

    # Ordenamiento
    if "sort_by" in request.args:
        data["sort_by"] = request.args.get("sort_by", "")

    # Si se quiere descargar el archivo
    if "download" in request.args:
        if request.args.get("download", "") == "Download":
            code = 200
            # Comenzar por la primera pagina
            page = 1
            list_seisms = []
            # Recorrer hasta que no haya mas paginas
            while code == 200:
                data["page"] = page
                # Llamada a la api
                req = sendRequest(method="get", url="/verified-seisms", data=json.dumps(data),)
                code = req.status_code
                if code == 200:
                    # Recorrer los sismos de la pagina y colocar los campos que se quieren agregar
                    for seism in json.loads(req.text)["Verified-Seisms"]:
                        element = {
                            "id": seism["id"],
                            "datetime": seism["datetime"],
                            "depth": seism["depth"],
                            "magnitude": seism["magnitude"],
                            "latitude": seism["latitude"],
                            "longitude": seism["longitude"],
                            "sensor.name": seism["sensor"]["name"],
                        }
                        # Agregar cada elemento a la lista
                        list_seisms.append(element)
                # Aumentar en uno el numero de pagina
                page += 1

            # Inicializar para poder escribir en el buffer de memoria
            si = io.StringIO()
            # Inicializar el objeto que va a escribir el csv a partir de un diccionario
            # Pasar las claves del diccionario como cabecera
            fc = csv.DictWriter(si, fieldnames=list_seisms[0].keys())
            # Escribir la cabecera
            fc.writeheader()
            # Escribir las filas
            fc.writerows(list_seisms)

            # Crear una respuesta que tiene como contenido el valor dedl buffer
            output = make_response(si.getvalue())
            # Colocar cabeceras para que se descargue como un archivo
            output.headers["Content-Disposition"] = "attachment; filename=seisms.csv"
            output.headers["Content-type"] = "text/csv"

            # Devolver la salida
            return output



    # Numero de pagina
    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]

    # Obtener datos de la api para la tabla
    req = sendRequest(method="get", url="/verified-seisms", data=json.dumps(data))
    if req.status_code == 200:
        # Cargar sismos verificados
        verified_seisms = json.loads(req.text)["Verified-Seisms"]
        # Cargar datos de paginacion
        pagination = {}
        pagination["total"] = json.loads(req.text)["total"]
        pagination["pages"] = json.loads(req.text)["pages"]
        pagination["current_page"] = json.loads(req.text)["page"]
        title = "Verified Seisms List"
        return render_template("verified-seisms.html", title=title, verified_seisms=verified_seisms, filter=filter, pagination=pagination,)

    else:
        return redirect(url_for("verified_seism.index"))

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

