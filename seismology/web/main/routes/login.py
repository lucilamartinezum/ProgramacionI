#from .. import login_manager
#from flask import request
#from flask_login import UserMixin, LoginManager
#import jwt

from flask import Blueprint, render_template
from ..forms.login import LoginForm
login = Blueprint('auth', __name__, url_prefix='/')


@login.route('/login')
def index():
    return render_template('login.html')


"""#Clase que contendrá los datos del usuario logueado
class User(UserMixin):
    def __init__(self ,id ,email ,role):
        self.id = id
        self.email = email
        self.role = role

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
            user = User(user_data["id"],user_data["email"],user_data["role"])
            #Devolver usuario logueado con los datos cargados
            return user
        except jwt.exceptions.InvalidTokenError:
            print('Invalid Token.')
        except jwt.exceptions.DecodeError:
            print('DecodeError.')
    return None"""
