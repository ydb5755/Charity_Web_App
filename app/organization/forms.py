from flask_wtf import FlaskForm
from wtforms import (SubmitField,
                    SelectField,
                    DateTimeLocalField,
                    DecimalField,
                    IntegerField,
                    StringField)
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flask_login import current_user
from datetime import datetime


class ConfirmAmountForm(FlaskForm):
    submit = SubmitField('Confirm Donation')

class SingleDonationForm(FlaskForm):
    amount = DecimalField('Amount:', render_kw={'placeholder': 'Amount'})
    submit = SubmitField('Donate!')

    def validate_amount(form, field):
        if field.data < .01:
            raise ValidationError('Amount should be at least .01')
        if current_user.balance < field.data:
            raise ValidationError('You do not have enough funds to make this donation')

class UpdateCharityInfoForm(FlaskForm):
    id               = IntegerField('Charity ID', validators=[DataRequired(), NumberRange(min=5000)])
    charity_name     = StringField('Charity Name', validators=[DataRequired()])
    address          = StringField('Address', validators=[DataRequired()])
    zip_code         = StringField('Zipcode', validators=[DataRequired()])
    phone            = StringField('Phone Number', validators=[DataRequired()])
    website          = StringField('Website')
    email            = StringField('Email', validators=[DataRequired()])
    contact_name     = StringField('Contact Name')
    contact_cell     = StringField('Contact Cell', validators=[DataRequired()])
    contact_position = StringField('Contact Position')
    bank             = StringField('Bank', validators=[DataRequired()])
    account_number   = StringField('Account Number', validators=[DataRequired()])
    submit           = SubmitField('Update Account')



class RecurringDonationForm(FlaskForm):
    amount = DecimalField('Amount:', places=2 ,render_kw={'placeholder': 'Amount'})
    how_often = SelectField('Frequency:', choices=['Minute', 'Hour', 'Day', 'Week', 'Month'])
    start = DateTimeLocalField('Start:', format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField('End:', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Donate!')

    def validate_end(form, field):
        if form.start.data is None or  form.end.data is None:
            raise ValidationError('Please enter a start and end time')
        start = int(form.start.data.timestamp())
        end = int(field.data.timestamp())
        if start > end:
            raise ValidationError('Your end date is earlier than the start. Please choose appropriate dates')
        if end < int(datetime.now().timestamp()):
            raise ValidationError('Your end date is in the past, please choose future dates')
        
    def validate_start(form, field):
        if form.start.data is None or  form.end.data is None:
            raise ValidationError('Please enter a start and end time')
        start = int(form.start.data.timestamp())
        end = int(field.data.timestamp())
        if start > end:
            raise ValidationError('Your end date is earlier than the start. Please choose appropriate dates')
        if start <= int(datetime.now().timestamp()):
            raise ValidationError('Your start date is in the past, please choose future dates')
        
    def validate_how_often(form, field):
        if form.start.data is None or  form.end.data is None:
            raise ValidationError('Please enter a start and end time')
        start_data = form.start.data
        end_data = form.end.data
        start = int(start_data.timestamp())
        end = int(end_data.timestamp())
        frequency = form.how_often.data
        total_time = end-start
        if start_data.year > end_data.year:
            raise ValidationError('Check your years')
        if frequency == 'Minute' or frequency == 'Second':
            if total_time < 60:
                raise ValidationError('You must choose start and end dates that are at least a minute apart')
        elif frequency == 'Hour':
            if total_time < 3600:
                raise ValidationError('You must choose start and end dates that are at least an hour apart')
        elif frequency == 'Day':
            if total_time < 86400:
                raise ValidationError('You must choose start and end dates that are at least a day apart')
        elif frequency == 'Week':
            if total_time < 604800:
                raise ValidationError('You must choose start and end dates that are at least a week apart')
        elif frequency == 'Month':
            years = (end_data.year-start_data.year)*12
            months = end_data.month-start_data.month
            if (end_data.day-start_data.day) < 0 or \
            (end_data.day-start_data.day) == 0 and end_data.time() < start_data.time():
                months -= 1
            total_months = years + months
            if total_months <= 0 or\
                total_months == 1 and start_data.day > end_data.day or\
                total_months == 1 and start_data.day == end_data.day and start_data.time() > end_data.time():
                raise ValidationError('You must choose start and end dates that are at least a month apart')
            if total_months > 12:
                raise ValidationError('We do not accept recurring donations longer than 12 months.')
        else:
            raise ValidationError('Something went wrong with the selection, please try again or try choosing another frequency')

                 

        
    def validate_amount(form, field):
        if form.start.data is None or  form.end.data is None:
            raise ValidationError('Please enter a start and end time')
        start = int(form.start.data.timestamp())
        end = int(form.end.data.timestamp())
        total_time = end-start
        amount = float(field.data)
        frequency = form.how_often.data
        if amount <= .009:
            raise ValidationError('Amount must be at least .01')
        if frequency == 'Second':
            total = total_time*amount
            if current_user.balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Minute':
            total = (total_time/60)*amount
            if current_user.balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Hour':
            total = (total_time/3600)*amount
            if current_user.balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Day':
            total = (total_time/86400)*amount
            if current_user.balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Week':
            total = (total_time/604800)*amount
            if current_user.balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Month':
            years = (form.end.data.year-form.start.data.year)*12
            months = form.end.data.month-form.start.data.month
            if (form.end.data.day-form.start.data.day) < 0 or \
                (form.end.data.day-form.start.data.day) == 0 and form.end.data.time() < form.start.data.time():
                months -= 1
            total_months = years + months
            if current_user.balance < total_months*amount:
                raise ValidationError('You do not have enough funds to make this pledge')
        else:
            raise ValidationError('Something went wrong with the selection, please try again or try choosing another frequency')
        
