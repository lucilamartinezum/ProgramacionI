import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api

import main.resources as resources

api = Api()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.SensorResource, '/sensor/<id>')
    api.add_resource(resources.VerifiedseismsResource, '/verified-seisms')
    api.add_resource(resources.VerifiedseismResource, '/verified-seism/<id>')
    api.add_resource(resources.UnverifiedseismsResource, '/unverified-seisms')
    api.add_resource(resources.UnverifiedseismResource, '/unverified-seism/<id>')
    api.init_app(app)
    return app