from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from functools import wraps


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['admin']:
            return fn(*args, **kwargs)
        else:
            return 'Only admins can access', 403
    return wrapper

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        "id": user.id,
        "email": user.email,
        "admin": user.admin,
    }