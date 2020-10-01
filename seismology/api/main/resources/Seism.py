from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel
from main.models import SensorModel
import time
from random import uniform, random, randint
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required

class Unverifiedseism(Resource):
    @jwt_required
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return 'Denied Access', 403
    @jwt_required#@admin_required
    # eliminar recurso
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return 'Unverifield seism was delete succesfully', 204
        else:
            return 'Denied Access', 403

    @jwt_required
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
    @jwt_required
    # obtener lista de recursos
    def get(self):
        page = 1
        per_page = 10
        max_per_page = 50
        #filtrar sismos no verificados

        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)
        try:
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'id':
                    seisms = seisms.filter(SeismModel.id == value)
                if key == 'sensorId':
                    seisms = seisms.filter(SeismModel.sensorId == value)
                #ORDENAMIENTO
                if key == "sort_by":
                    if value == "datetime.desc":
                        seisms = seisms.order_by(SeismModel.datetime.desc())
                    if value == "datetime.asc":
                        seisms = seisms.order_by(SeismModel.datetime.asc())
                #PAGINACION

                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
        except:
            pass

        seisms = seisms.paginate(page, per_page, True, max_per_page)
        return jsonify({'Unverified-Seisms': [seism.to_json() for seism in seisms.items]})
    @admin_required
    def post(self):
        sensors = db.session.query(SensorModel).all()
        sensorsId = []
        for sensor in sensors:
            sensorsId.append(sensor.id)

        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': False,
            'sensorId': sensorsId[randint(0, len(sensorsId) - 1)]
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201

class Verifiedseism(Resource):
    #@jwt_required
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism.to_json()
        else:
            return 'Denied Access', 403

class Verifiedseisms(Resource):
    #@jwt_required
    # obtener lista de recursos
    def get(self):
        page = 1
        per_page = 25
        max_per_page = 10000


        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        try:
            # filtro para sismos verificados
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'sensor.name':
                    seisms = seisms.join(SeismModel.sensor).filter(SensorModel.name.like('%'+value+'%'))
                if key == 'magnitude':
                    seisms = seisms.filter(SeismModel.magnitude == value)
                if key == 'datetime':
                    seisms = seisms.filter(SeismModel.datetime == value)
                #ORDENAMIENTO

                if key == "sort_by":
                    if value == "datetime.desc":
                        seisms = seisms.order_by(SeismModel.datetime.desc())
                    if value == "datetime.asc":
                        seisms = seisms.order_by(SeismModel.datetime.asc())
                    if value == "sensor.name.desc":
                        seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                    if value == "sensor.name.asc":
                        seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())

                #PAGINACION
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
        except:
            pass

        seisms = seisms.paginate(page, per_page, True, max_per_page)  #True para no mostrar error
        return jsonify({'Verified-Seism': [seism.to_json() for seism in seisms.items]})

    """
    @jwt_required
    #crea sismos verificados para testear en la db
    def post(self):
        sensors = db.session.query(SensorModel).all()
        sensorsId = []
        for sensor in sensors:
            sensorsId.append(sensor.id)
        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': True,
            'sensorId': sensorsId[randint(0, len(sensorsId) - 1)]
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201
    """