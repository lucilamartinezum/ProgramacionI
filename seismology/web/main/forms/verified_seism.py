from flask_wtf import FlaskForm
from wtforms import HiddenField, FloatField, IntegerField, SubmitField, StringField
from wtforms import validators  # Importa validaciones
from wtforms.fields.html5 import DateTimeLocalField as DateTimeField

class VerifiedSeismsFilter(FlaskForm):

    from_datetime = DateTimeField(
        label="Since date",
        validators=[validators.optional()]
        )

    to_datetime = DateTimeField(
        label="Until date",
        validators=[validators.optional()]
        )

    depth_min = IntegerField(
        label="Depth min",
        validators=[validators.optional()]
        )

    depth_max = IntegerField(
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

    sensor_name = StringField(
        label="Associated sensor",
        validators=[validators.optional()])

    sort_by = HiddenField()

    per_page = IntegerField(
        validators=[validators.optional()]
        )

    submit = SubmitField(
        label="Filter",
    )
