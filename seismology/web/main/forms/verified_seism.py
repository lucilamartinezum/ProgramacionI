from flask_wtf import FlaskForm
from wtforms import HiddenField, FloatField, IntegerField, SubmitField, StringField, SelectField
from wtforms import validators  # Importa validaciones
from wtforms.fields.html5 import DateTimeLocalField as DateTimeField

class VerifiedSeismsFilter(FlaskForm):

    from_datetime = DateTimeField(
        label="Since date",format='%Y-%m-%dT%H:%M',
        validators=[validators.optional()]
        )

    to_datetime = DateTimeField(
        label="Until date",format='%Y-%m-%dT%H:%M',
        validators=[validators.optional()]
        )

    depth_min = FloatField(
        label="Depth min",
        validators=[validators.optional()]
        )

    depth_max = FloatField(
        label="Depth max",
        validators=[validators.optional()]
        )

    magnitude_min = FloatField(
        label="Magnitude min",
        validators=[validators.optional()]
        )
    magnitude_max = FloatField(
        label="Magnitude max",
        validators=[validators.optional()]
        )

    sensor_name = SelectField(
        label="Associated sensor",
        validators=[validators.optional()])

    sensorId = SelectField(
        label="Associated sensor",
        coerce= int,
        validators=[validators.optional()])


    per_page = IntegerField(
        validators=[validators.optional()]
        )

    submit = SubmitField(label="Filter",)

    download = SubmitField("Download")
