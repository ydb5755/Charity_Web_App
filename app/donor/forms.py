from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class AddAdmin(FlaskForm):
    id = StringField('User ID')
    submit = SubmitField('Add Admin')

class RemoveAdmin(FlaskForm):
    admin = SelectField('Select Admin to remove priviliges')
    submit = SubmitField('Remove Admin')