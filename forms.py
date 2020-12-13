from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField

class DateForm(FlaskForm):
  date = DateField('Pick a Date', format="%m/%d/%Y")
  submit = SubmitField('Submit')