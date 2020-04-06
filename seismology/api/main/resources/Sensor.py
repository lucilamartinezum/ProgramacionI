from flask_restful import Resource
from flask import request

SENSORS = {
    1: {"name": "sensor1", "status": "verificado"},
    2: {"name": "sensor2", "status": "no verificado"},
}

class Sensor(Resource):
    #obtener recurso
    def get(self, id):
        if int(id) in SENSORS:
            return SENSORS[int(id)]
        return 'Sensor not found', 404

    #eliminar recurso
    def delete(self, id):
        if int(id) in SENSORS:
            del SENSORS[int(id)]
            return '', 204
        return 'Sensor not found', 404

    #modificar recurso
    def put(self, id):
        if int(id) in SENSORS:
            sensor = SENSORS[int(id)]
            data = request.get_json()
            sensor.update(data)
            return sensor, 201
        return 'Sensor not found', 404

class Sensors(Resource):
    #obtener lista de recursos
    def get(self):
        return SENSORS

    #insertar recurso
    def post(self):
        sensor = request.get_json()
        print(SENSORS.keys())
        print(max(SENSORS.keys()))
        id = int(max(SENSORS.keys())) + 1
        SENSORS[id] = sensor
        return SENSORS[id], 201