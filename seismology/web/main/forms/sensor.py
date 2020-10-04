from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField, HiddenField
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

class SensorFilter(FlaskForm):
    name = StringField(
        label="Name",
        validators=[validators.optional()],
    )
    status = BooleanField(
        label="Status: Working?",
        validators=[validators.optional()],
    )
    active = BooleanField(
        label="Active",
        validators=[validators.optional()],
    )
    user_email = StringField(
        label="User email",
        validators=[validators.optional()]
    )

    sort_by = HiddenField()


    elem_per_page = IntegerField(
        validators=[validators.optional()]
    )

    submit = SubmitField(
        label="Filter",
    )


