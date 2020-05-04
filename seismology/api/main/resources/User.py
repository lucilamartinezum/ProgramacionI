from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, jwt_optional

class User(Resource):

    @jwt_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    @jwt_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    @jwt_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return '', 409
        return "User was deleted succesfully", 204

class Users(Resource):

    @jwt_required
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify({'Users': [user.to_json() for user in users]})






