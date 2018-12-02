from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


def asin_validation_check(form, field):
    field.data = field.data.strip().upper()
    if len(field.data) != 10:
        raise ValidationError("Invalid ASIN")


class Asin_search_form(FlaskForm):
    asin = StringField("ASIN", validators=[DataRequired(), asin_validation_check])
    submit = SubmitField("Submit")
