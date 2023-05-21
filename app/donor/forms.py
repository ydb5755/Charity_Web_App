from flask_wtf import FlaskForm
from wtforms import (StringField, 
                     SubmitField, 
                     SelectField, 
                     IntegerField, 
                     FloatField, 
                     EmailField, 
                     PasswordField)
from wtforms.validators import DataRequired, ValidationError, NumberRange, Email, EqualTo
from app.models import Donor, Charity

class AddAdmin(FlaskForm):
    id = IntegerField('User ID', validators=[DataRequired()], render_kw={'placeholder': 'ID'})
    submit = SubmitField('Add!')

    def validate_id(form, field):
        donor = Donor.query.filter_by(id=field.data).first()
        if not donor:
            raise ValidationError('This user does not exist, try another id')
        if donor.admin == True:
            raise ValidationError('This user is already an admin')
        

class RemoveAdmin(FlaskForm):
    admin = SelectField('Select Admin to remove priviliges', validators=[DataRequired()])
    submit = SubmitField('Remove')

class AddFunds(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)], render_kw={'placeholder': 'Amount'})
    cc_number = StringField('Card Number')
    expiry_date = StringField('Expiry Date')
    sec_code = StringField('Security Code')
    tz = StringField('Israeli ID Number')
    submit = SubmitField('Add Funds')

class UpdateDonorInfoForm(FlaskForm):
    first_name       = StringField('First Name', validators=[DataRequired()])
    last_name        = StringField('Last Name', validators=[DataRequired()])
    address          = StringField('Address', validators=[DataRequired()])
    zip_code         = StringField('Zipcode', validators=[DataRequired()])
    phone_home       = StringField('Phone Home')
    phone_cell       = StringField('Phone Cell', validators=[DataRequired()])
    email            = EmailField('Email', validators=[DataRequired()])
    password         = PasswordField('Enter a password')
    confirm_password = PasswordField('Confirm your password')
    submit           = SubmitField('Update Account')

