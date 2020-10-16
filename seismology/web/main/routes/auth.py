from .. import login_manager
from flask import request, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, current_user
import jwt
from functools import wraps



class User(UserMixin): #Clase que contendrá los datos del usuario logueado
    def __init__(self, id, email, admin):
        self.id = id
        self.email = email
        self.admin = admin

#Método que le indica a LoginManager como obtener los datos del usuario logueado
#En nuestro caso al trabajar con JWT los datos se obtendran de los claims del Token
#que ha sido guardado en una cookie en el browser
@login_manager.request_loader
def load_user(request):
    #Verificar si la cookie ha sido cargada
    if 'access_token' in request.cookies:
        try:
            #Decodificar el token
            decoded = jwt.decode(request.cookies['access_token'], verify=False)
            user_data = decoded["user_claims"]
            #Cargar datos del usuario
            try:
                user = User(user_data["id"], user_data["email"], user_data["admin"])
                return user
            except KeyError:
                return redirect(url_for('login.index'))

        except jwt.exceptions.InvalidTokenError:
            print('Invalid Token.')
        except jwt.exceptions.DecodeError:
            print('DecodeError.')
    return None


#Función que sobreescribe el método al intentar ingresar a una ruta no autorizada
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must log in to continue.','warning')
    #Redireccionar a la página que contiene el formulario de login
    return redirect(url_for('main.index'))


#Define la función de verificación de admin para las rutas
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        if not current_user.admin:
            flash('Access restricted to administrators.','warning')
            return redirect(url_for('main.index'))
        return fn(*args, **kws)
    return wrapper