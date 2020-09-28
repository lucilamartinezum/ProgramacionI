from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms import validators


class SensorForm(FlaskForm):
    name = StringField(
        label="Name",
        validators=[validators.DataRequired(message="This field is required")]
    )

    ip = StringField(
        label="IP",
        validators=[validators.DataRequired(message="This field is required")]
    )

    port = IntegerField(
        label="Port",
        validators=[validators.InputRequired(message="This field is required")]
    )

    status = BooleanField(label="Status: Working?")

    active = BooleanField(label="Active")

    userId = SelectField(
        label="User Associated",
        validators=[validators.InputRequired(
            message="This field is required")],
        coerce=int #el parametro tiene que ser un valor entero
    )

    submit = SubmitField(label="Add")


class SensorEdit(FlaskForm):
    name = StringField(
        label="Name",
        validators=[validators.DataRequired(message="This field is required")]
    )

    ip = StringField(
        label="IP",
        validators=[validators.DataRequired(message="This field is required")]
    )

    port = IntegerField(
        label="Port",
        validators=[validators.InputRequired(message="This field is required")]
    )

    status = BooleanField(label="Status")

    active = BooleanField(label="Active")

    userId = SelectField(
        label="User Associated",
        validators=[validators.InputRequired(
            message="This field is required")],
        coerce=int
    )

    submit = SubmitField(label="Send")
