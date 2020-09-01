from flask_wtf import FlaskForm # Importa funciones de formulario
from wtforms import PasswordField,SubmitField, BooleanField # Importa campos
from wtforms.fields.html5 import EmailField # Importa campos HTML
from wtforms import validators # Importa validaciones

class UserForm(FlaskForm):

    # Definicion de campo Email
    email = EmailField("E-mail", [
        validators.Required(message = "E-mail is require"),
        validators.Email(message = "Format not valid"),
    ])

    # Definicion de campo Contraseña
    password = PasswordField("Password", [
        validators.Required(),
        # El campo de contraseña debe coincidir con el de confirmar
        validators.EqualTo("confirm", message = "Passwords dont match")
    ])

    confirm = PasswordField("Repeat Password")

    admin = BooleanField("Admin?")

    # Definicion de campo Sumbit
    submit = SubmitField("Send")

class UserEdit(FlaskForm):

    # Definicion de campo Email
    email = EmailField("E-mail", [
        validators.Required(message = "E-mail is required"),
        validators.Email(message = "Format not valid"),
    ])

    # Definicion de campo Admin
    admin = BooleanField("Admin")

    # Definicion de campo Sumbit
    submit = SubmitField("Send")