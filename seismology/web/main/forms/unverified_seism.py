from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, SubmitField, StringField
from wtforms import validators  # Importa validaciones
#from wtforms.fields.html5 import DateTimeLocalField as DateTimeField

class UnverifiedSeismEdit(FlaskForm):

    latitude = StringField(
        label="Latitude",
        validators=[validators.DataRequired(message="This field is required")]
    )

    longitude = StringField(
        label="Longitude",
        validators=[validators.DataRequired(message="This field is required")]
    )
    # Definicion de campo Integer
    depth = IntegerField(
        label="Depth",
        validators=[validators.DataRequired(message="This field should be an integer")])

    # Definicion de campo Float
    magnitude = FloatField(
        label="Magnitude",
        validators=[validators.DataRequired(message="This field should be a decimal value")])

    # Definicion de campo CheckBox
    verified = BooleanField()

    # Definicion de campo Sumbit
    submit = SubmitField("Send")