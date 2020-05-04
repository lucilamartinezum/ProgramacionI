from flask import request, jsonify, Blueprint
from main import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, jwt_optional

auth = Blueprint('auth', __name__, url_prefix= '/auth')

@auth.route('/login', methods = ['POST'])
def login():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get('email')).first_or_404()
    if user.validate_pass(request.get_json().get('password')):
        access_token = create_access_token(identify = user)
        data = '{"id":"'+str(user.id)+'", "email":"'+str(user.email)+'", "access_token":"'+access_token+'"}'
        return  data, 200
    else:
        return 'Incorrect password', 204
@auth.route('/register', methods = ['POST'])
def register():
    user = UserModel.from_json(request.get_json())
    exists = db.session.query(UserModel).filter(UserModel.id == user.id).scalar() is not None
    if exists:
        return 'Duplicate email', 409
    else:
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201