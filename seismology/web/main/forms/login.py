# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField #Importa campos
from wtforms.fields.html5 import EmailField, DateTimeField #Importa campos HTML
from wtforms import validators #Importa validaciones

class LoginForm(FlaskForm):

    email = EmailField('E-mail',
    [
        validators.Required(message = "E-mail is require"),
        validators.Email( message ='Formad not valid'),
    ])

    #Definición de campo de contraseña
    password = PasswordField('Password', [
        validators.Required(),
    ])
    #Definición de campo submit
    submit = SubmitField("Send")