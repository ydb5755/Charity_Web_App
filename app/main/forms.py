from flask_wtf import FlaskForm
from wtforms import StringField, \
                    EmailField, \
                    PasswordField, \
                    SubmitField, \
                    SelectField, \
                    BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    type_of_user = SelectField(choices=['Donor', 'Charity'])
    email        = EmailField('Email', validators=[DataRequired()])
    password     = PasswordField('Password', validators=[DataRequired()])
    remember     = BooleanField('Remember me')
    submit       = SubmitField('Login')

class DonorSignUpForm(FlaskForm):
    first_name       = StringField('First Name', validators=[DataRequired()])
    last_name        = StringField('Last Name', validators=[DataRequired()])
    address          = StringField('Address', validators=[DataRequired()])
    zip_code          = StringField('Zipcode', validators=[DataRequired()])
    phone_home       = StringField('Phone Home')
    phone_cell       = StringField('Phone Cell', validators=[DataRequired()])
    email            = EmailField('Email', validators=[DataRequired()])
    password         = PasswordField('Enter a password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm your password', validators=[DataRequired()])
    submit           = SubmitField('Sign Up')

class CharitySignUpForm(FlaskForm):
    id               = StringField('Charity ID', validators=[DataRequired()])
    charity_name     = StringField('Charity Name', validators=[DataRequired()])
    address          = StringField('Address', validators=[DataRequired()])
    zip_code         = StringField('Zipcode', validators=[DataRequired()])
    phone            = StringField('Phone Number', validators=[DataRequired()])
    website          = StringField('Website')
    email            = StringField('Email', validators=[DataRequired()])
    password         = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm your password', validators=[DataRequired()])
    contact_name     = StringField('Contact Name')
    contact_cell     = StringField('Contact Cell', validators=[DataRequired()])
    contact_position = StringField('Contact Position')
    bank             = StringField('Bank', validators=[DataRequired()])
    account_number   = StringField('Account Number', validators=[DataRequired()])
    submit           = SubmitField('Sign Up')