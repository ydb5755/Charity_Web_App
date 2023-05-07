from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    type_of_user = SelectField(choices=['Donor', 'Charity'])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

