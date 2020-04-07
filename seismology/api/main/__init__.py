import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy



api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    if not os.path.exist(os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME')):
        os.mknod(os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME')
    db.init_app(app)
    import main.resources as resources
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.SensorResource, '/sensor/<id>')
    api.add_resource(resources.VerifiedseismsResource, '/verified-seisms')
    api.add_resource(resources.VerifiedseismResource, '/verified-seism/<id>')
    api.add_resource(resources.UnverifiedseismsResource, '/unverified-seisms')
    api.add_resource(resources.UnverifiedseismResource, '/unverified-seism/<id>')
    api.init_app(app)
    return app