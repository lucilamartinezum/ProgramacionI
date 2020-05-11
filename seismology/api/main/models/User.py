from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, index = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    admin = db.Column(db.Boolean, nullable = False)
    #relation with sensors
    sensors = db.relationship("Sensor", back_populates="user")

    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')
    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)
    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<Users: %r %r %r>" % (self.id, self.email, self.admin)

    def to_json(self):
        user_json = {
            'id': self.id,
            'email': str(self.email),
            'admin': self.admin,
        }
        return user_json
    def to_json_public(self):
        user_json = {
            'email': str(self.email),
        }
        return user_json

    def from_json(user_json):
        id = user_json.get('id')
        email = user_json.get('email')
        password = user_json.get('password')
        admin = user_json.get('admin')
        return User(id = id, email = email, plain_password = password, admin = admin)