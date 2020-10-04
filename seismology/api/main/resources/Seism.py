from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel
from main.models import SensorModel
import time, datetime
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
        raise_error = True
        #filtrar sismos no verificados
        filters = request.get_json().items()
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)

        for key, value in filters:
            if key == 'sensorId':
                seisms = seisms.join(SeismModel.sensor).filter(SensorModel.id == value)
            if key == "from_date":
                seisms = seisms.filter(SeismModel.datetime >= value)
            if key == "to_date":
                seisms = seisms.filter(SeismModel.datetime <= value)

            # ORDENAMIENTO
            if key == "sort_by":
                if value == "sensor.name.desc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                if value == "sensor.name.asc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())

                if value == "datetime.desc":
                    seisms = seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime.asc":
                    seisms = seisms.order_by(SeismModel.datetime.asc())

                if value == "magnitude.desc":
                    seisms = seisms.order_by(SeismModel.magnitude.desc())
                if value == "magnitude.asc":
                    seisms = seisms.order_by(SeismModel.magnitude.asc())

            # PAGINACION

            if key == "page":
                page = int(value)
            if key == "per_page":
                per_page = int(value)

        seisms = seisms.paginate(page, per_page, True, max_per_page, raise_error)
        return jsonify({'Unverified-Seisms': [seism.to_json() for seism in seisms.items],
                        'total': seisms.total,
                        'pages': seisms.pages,
                        'page': page,
                        'per_page': per_page
                        })


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

        filters = request.get_json().items()
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        # filtro para sismos verificados

        for key, value in filters:
            # Filtros
            if key == "from_date":
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                seisms = seisms.filter(SeismModel.datetime >= value)
            if key == "to_date":
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                seisms = seisms.filter(SeismModel.datetime <= value)
            if key == "mag.min":
                seisms = seisms.filter(SeismModel.magnitude >= value)
            if key == "mag.max":
                seisms = seisms.filter(SeismModel.magnitude <= value)
            if key == "depth.min":
                seisms = seisms.filter(SeismModel.depth >= value)
            if key == "depth.max":
                seisms = seisms.filter(SeismModel.depth <= value)
            if key == "sensor.name":
                seisms = seisms.join(SeismModel.sensor).filter(SensorModel.name.like("%" + str(value) + "%"))

            # ORDER
            if key == "sort_by":
                if value == "datetime.desc":
                    seisms = seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime.asc":
                    seisms = seisms.order_by(SeismModel.datetime.asc())
                if value == "sensor.name.desc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                if value == "sensor.name.asc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())
                if value == "magnitude.desc":
                    seisms = seisms.order_by(SeismModel.magnitude.desc())
                if value == "magnitude.asc":
                    seisms = seisms.order_by(SeismModel.magnitude.asc())
                if value == "depth.desc":
                    seisms = seisms.order_by(SeismModel.depth.desc())
                if value == "depth.asc":
                    seisms = seisms.order_by(SeismModel.depth.asc())

            # PAGINACION
            if key == "page":
                page = int(value)
            if key == "per_page":
                per_page = int(value)

        seisms = seisms.paginate(page, per_page, True, max_per_page)  # True para no mostrar error
        return jsonify({'Verified-Seism': [seism.to_json() for seism in seisms.items],
                        'total': seisms.total,
                        'pages': seisms.pages,
                        'page': page,
                        'per_page': per_page})



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