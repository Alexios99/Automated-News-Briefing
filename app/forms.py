from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class GenerateBriefingForm(FlaskForm):
    days_ago = IntegerField('Look back days', default=3, validators=[DataRequired(), NumberRange(min=1, max=30)])
    custom_keywords = StringField('Custom Keywords (comma-separated)', validators=[Optional()])
    submit = SubmitField('Generate Briefing') 