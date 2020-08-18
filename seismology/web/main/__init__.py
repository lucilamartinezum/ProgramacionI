import os
from flask import Flask
from dotenv import load_dotenv
from flask_breadcrumbs import Breadcrumbs
from flask_wtf import CSRFProtect #importar para proteccion CSRF

def create_app():
    app = Flask(__name__)
    Breadcrumbs(app=app)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')
    csrf = CSRFProtect(app)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    print(app.config["SECRET_KEY"])
    from main.routes import main, unverified_seism
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.unverified_seism.unverified_seism)
    return app
