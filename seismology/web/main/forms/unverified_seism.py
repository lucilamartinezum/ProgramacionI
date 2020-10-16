from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, SubmitField, HiddenField, SelectField
from wtforms import validators  # Importa validaciones
from wtforms.fields.html5 import DateTimeLocalField as DateTimeField

class UnverifiedSeismEdit(FlaskForm):

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


class UnverifiedSeismsFilter(FlaskForm):

    sensorId = SelectField(
        label="Sensor name",
        validators=[validators.optional()],
        coerce=int)

    from_datetime = DateTimeField(
        label="Since date", format='%Y-%m-%dT%H:%M',
        validators=[validators.optional()]
    )

    to_datetime = DateTimeField(
        label="Until date", format='%Y-%m-%dT%H:%M',
        validators=[validators.optional()]
    )

    sort_by = HiddenField()


    per_page = IntegerField(
        validators=[validators.optional()]
    )

    submit = SubmitField(
        label="Filter",
    )
