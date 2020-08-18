from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required

class Sensor(Resource):
    @jwt_required
    #obtener recurso
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()
    @admin_required
    #eliminar recurso
    def delete(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return '', 409
        return "Sensor was deleted succesfully", 204
    @admin_required
    #modificar recurso
    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(sensor, key, value)
        db.session.add(sensor)
        try:
            db.session.commit()
            return sensor.to_json(), 201
        except Exception as error:
            return str(error), 400


class Sensors(Resource):
    @jwt_required
    #obtener lista de recursos
    def get(self):
        page = 1
        per_page = 25
        max_per_page = 50
        #filtrar sensores
        filters = request.get_json().items()
        sensors = db.session.query(SensorModel)
        try:
            for key, value in filters:
                if key == 'userId':
                    sensors = sensors.filter(SensorModel.userId == value)
                if key == 'active':
                    sensors = sensors.filter(SensorModel.active == value)
                if key == 'status':
                    sensors = sensors.filter(SensorModel.status == value)
                #Filtro user email
                if key == 'user.email':
                    sensors = sensors.join(SensorModel.user).filter(UserModel.email.like('%'+value+'%'))
                # ORDENAMIENTO

                if key == "sort_by":
                    if value == "name.desc":
                        sensors = sensors.order_by(SensorModel.name.desc())
                    if value == "name.asc":
                        sensors = sensors.order_by(SensorModel.name.asc())
                    if value == "userId.desc":
                        sensors = sensors.order_by(SensorModel.userId.desc())
                    if value == "userId.asc":
                        sensors = sensors.order_by(SensorModel.userId.asc())
                    if value == "active.desc":
                        sensors = sensors.order_by(SensorModel.active.desc())
                    if value == "active.asc":
                        sensors = sensors.order_by(SensorModel.active.asc())
                    if value == "status.desc":
                        sensors = sensors.order_by(SensorModel.status.desc())
                    if value == "status.asc":
                        sensors = sensors.order_by(SensorModel.status.asc())
                #ORDENAMIENTO POR EMAIL
                    if value == "user.email.desc":
                        sensors = sensors.join(SensorModel.user).order_by(UserModel.email.desc())
                    if value == "user.email.asc":
                        sensors = sensors.join(SensorModel.user).order_by(UserModel.email.asc())

                #PAGINACION
                if key == "page":
                    page = value
                if key == "per_page":
                    per_page = value
        except:
            pass

        sensors = sensors.paginate(page, per_page, True, max_per_page)
        return jsonify({'Sensors': [sensor.to_json() for sensor in sensors.items]})
    @admin_required
    #insertar recurso
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        try:
            db.session.add(sensor)
            db.session.commit()
        except Exception as error:
            return str(error), 400
        return sensor.to_json(), 201