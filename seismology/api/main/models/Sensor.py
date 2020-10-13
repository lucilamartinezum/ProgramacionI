from .. import db
from main.models.User import User

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    ip = db.Column(db.String(100), nullable = False)
    port = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Boolean, nullable = False)
    active = db.Column(db.Boolean, nullable = False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
    user = db.relationship("User", back_populates="sensors", uselist = False, single_parent = True)
    seisms = db.relationship("Seism", back_populates="sensor", passive_deletes = 'all')
    def __repr__(self):
        return "<Sensor: %r %r %r %r %r %r>" % (self.id, self.name, self.ip, self.port, self.status, self.active)
    def to_json(self):
        self.user = db.session.query(User).get(self.userId)
        try:
            sensor_json = {
                'id': self.id,
                'name': str(self.name),
                'ip': str(self.ip),
                'port': self.port,
                'status': self.status,
                'active': self.active,
                'user': self.user.to_json(),
            }
        except AttributeError:
            sensor_json = {
                'id': self.id,
                'name': str(self.name),
                'ip': str(self.ip),
                'port': self.port,
                'status': self.status,
                'active': self.active,
                'user': None,
            }
        return sensor_json
    def from_json(sensor_json):
        id = sensor_json.get('id')
        name = sensor_json.get('name')
        ip = sensor_json.get('ip')
        port = sensor_json.get('port')
        status = sensor_json.get('status')
        active = sensor_json.get('active')
        userId = sensor_json.get('userId')
        return Sensor(id = id, name = name, ip = ip, port = port, status = status, active = active, userId = userId)

    def to_json_public(self):
        sensor_json = {
            'id': self.id,
            'name': str(self.name),
        }

        return sensor_json
