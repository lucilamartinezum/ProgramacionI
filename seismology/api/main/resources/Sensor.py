from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel


class Sensor(Resource):
    #obtener recurso
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    #eliminar recurso
    def delete(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)
        db.session.commit()
        return "Sensor was deleted succesfully", 204

    #modificar recurso
    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(sensor,key, value)
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201

class Sensors(Resource):
    #obtener lista de recursos
    def get(self):
        sensors = db.session.query(SensorModel).all()
        return jsonify({'Sensors': [sensor.to_json() for sensor in sensors]})

    #insertar recurso
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201