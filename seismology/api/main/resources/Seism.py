from flask_restful import Resource
from flask import request

SEISMS = {
    1: {"ID": "1", "datetime": "02/01/2020", "magnitude": "2.51"},
    2: {"ID": "2", "datetime": "04/03/2020", "magnitude": "1.25"},
}


class Unverifiedseism(Resource):
    # obtener recurso
    def get(self, id):
        if int(id) in SEISMS:
            return SEISMS[int(id)]
        return 'Seism not found', 404

    # eliminar recurso
    def delete(self, id):
        if int(id) in SEISMS:
            del SEISMS[int(id)]
            return '', 204
        return 'Seism not found', 404

    # modificar recurso
    def put(self, id):
        if int(id) in SEISMS:
            seism = SEISMS[int(id)]
            data = request.get_json()
            seism.update(data)
            return seism, 201
        return 'Seism not found', 404


class Unverifiedseisms(Resource):
    # obtener lista de recursos
    def get(self):
        return SEISMS


class Verifiedseism(Resource):
    # obtener recurso
    def get(self, id):
        if int(id) in SEISMS:
            return SEISMS[int(id)]
        return 'Seism not found', 404
class Verifiedseisms(Resource):
    # obtener lista de recursos
    def get(self):
        return SEISMS