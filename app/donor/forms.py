from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class AddAdmin(FlaskForm):
    id = StringField('User ID', validators=[DataRequired()])
    submit = SubmitField('Add Admin')

class RemoveAdmin(FlaskForm):
    admin = SelectField('Select Admin to remove priviliges', validators=[DataRequired()])
    submit = SubmitField('Remove Admin')

class AddFunds(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Funds')