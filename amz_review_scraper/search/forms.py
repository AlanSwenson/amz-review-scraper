from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class Asin_search_form(FlaskForm):
    asin = StringField("ASIN", validators=[DataRequired(), Length(10)])
    submit = SubmitField("Submit")
