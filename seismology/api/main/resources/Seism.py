from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel
import time
from random import uniform, random, randint

class Unverifiedseism(Resource):
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return 'Denied Access', 403

    # eliminar recurso
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return 'Unverifield seism was delete succesfully', 204
        else:
            return 'Denied Access', 403

    # modificar recurso
    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            for key, value in request.get_json().items():
                setattr(seism, key, value)
            db.session.add(seism)
            db.session.commit()
            return seism.to_json(), 201
        else:
            return 'Denied Access', 403


class Unverifiedseisms(Resource):
    # obtener lista de recursos
    def get(self):
        #filtrar sismos no verificados
        filters = request.get_json().items()
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)
        for key, value in filters:
            if key == 'sensorId':
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == 'magnitude':
                seisms = seisms.filter(SeismModel.magnitude == value)
            if key == 'id':
                seisms = seisms.filter(SeismModel.id == value)
        seisms.all()
        return jsonify({'Unverified-Seisms': [seism.to_json() for seism in seisms]})

    def post(self):

        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': False,
            'sensorId': 2,
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201

class Verifiedseism(Resource):
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism.to_json()
        else:
            return 'Denied Access', 403

class Verifiedseisms(Resource):
    # obtener lista de recursos
    def get(self):
        #filtro para sismos verificados
        filters = request.get_json().items()
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        for key, value in filters:
            if key == 'sensorId':
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == 'magnitude':
                seisms = seisms.filter(SeismModel.magnitude == value)
            if key == 'id':
                seisms = seisms.filter(SeismModel.id == value)
        seisms.all()
        return jsonify({'Verified-Seism': [seism.to_json() for seism in seisms]})

    def post(self):
        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': True,
            'sensorId': 2,
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201