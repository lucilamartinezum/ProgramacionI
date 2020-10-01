from .. import db
from . import SensorModel
from datetime import datetime as dt

class Seism(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.DateTime, nullable = False)
    depth = db.Column(db.Integer, nullable = False)
    magnitude = db.Column(db.Float, nullable = False)
    latitude = db.Column(db.String(100), nullable = False)
    longitude = db.Column(db.String(100), nullable = False)
    verified = db.Column(db.Boolean, nullable = False)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete = 'RESTRICT'), nullable = False)
    sensor = db.relationship("Sensor", back_populates="seisms", uselist=False, single_parent=True)

    def __repr__(self):
        return '<Seism: %r %r %r %r %r %r %r>' % (self.id, self.datetime, self.depth, self.magnitude, self.latitude, self.longitude, self.verified)

    def to_json(self):
        self.sensor = db.session.query(SensorModel).get_or_404(self.sensorId)
        seism_json = {
            'id': self.id,
            'datetime': self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'depth': int(self.depth),
            'magnitude': str(self.magnitude),
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'verified': bool(self.verified),
            'sensor': self.sensor.to_json(),
        }
        return seism_json
    @staticmethod
    def from_json(seism_json):
        id = seism_json.get('id')
        datetime = dt.strptime(seism_json.get('datetime'), "%Y-%m-%d %H:%M:%S")
        depth = seism_json.get('depth')
        magnitude = seism_json.get('magnitude')
        latitude = seism_json.get('latitude')
        longitude = seism_json.get('longitude')
        verified = seism_json.get('verified')
        sensorId = seism_json.get('sensorId')
        return Seism(id = id, datetime = datetime, depth = depth, magnitude = magnitude, latitude = latitude, longitude = longitude,verified = verified, sensorId = sensorId)