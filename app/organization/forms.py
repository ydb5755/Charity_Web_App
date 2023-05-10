from flask_wtf import FlaskForm
from wtforms import StringField,\
                    EmailField,\
                    PasswordField,\
                    SubmitField,\
                    SelectField,\
                    BooleanField,\
                    DateTimeField,\
                    DateField,\
                    TimeField,\
                    DateTimeLocalField,\
                    IntegerField,\
                    DecimalField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flask_login import current_user


class SingleDonationForm(FlaskForm):
    amount = DecimalField('How much would you like to donate?')
    submit = SubmitField('Donate')

    def validate_amount(form, field):
        if field.data < .01:
            raise ValidationError('Amount should be at least .01')
        if current_user.current_balance < field.data:
            raise ValidationError('You do not have enough funds to make this donation')
        

class RecurringDonationForm(FlaskForm):
    amount = StringField('How much would you like to donate?')
    how_often = SelectField('How often would you like to make this payment?', choices=['Second', 'Minute', 'Hour', 'Day', 'Week', 'Month'])
    start = DateTimeLocalField('When should the payments start?', format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField('When should the payments end?', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Donate')

    def validate_end(form, field):
        start = form.start.data.timestamp().__floor__()
        end = field.data.timestamp().__floor__()
        if start > end:
            raise ValidationError('Your end date is earlier than the start. Please choose appropriate dates')
        
    def validate_how_often(form, field):
        start = form.start.data.timestamp().__floor__()
        end = form.end.data.timestamp().__floor__()
        frequency = form.how_often.data
        total_time = end-start
        if form.start.data.year >= form.end.data.year:
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
            if form.start.data.month >= form.end.data.month:
                raise ValidationError('You must choose start and end dates that are at least a month apart')

        else:
            raise ValidationError('Something went wrong with the selection, please try again or try choosing another frequency')

                # 2023-05-01 to 2022-04-31 == GOOD

        
    def validate_amount(form, field):
        start = form.start.data.timestamp().__floor__()
        end = form.end.data.timestamp().__floor__()
        total_time = end-start
        amount = float(field.data)
        frequency = form.how_often.data
        if amount <= .009:
            raise ValidationError('Amount must be at least .01')
        if frequency == 'Second':
            total = total_time*amount
            if current_user.current_balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Minute':
            total = (total_time/60)*amount
            if current_user.current_balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Hour':
            total = (total_time/3600)*amount
            if current_user.current_balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Day':
            total = (total_time/86400)*amount
            if current_user.current_balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Week':
            total = (total_time/604800)*amount
            if current_user.current_balance < total:
                raise ValidationError('You do not have enough funds to make this pledge')
        elif frequency == 'Month':
            years = (form.end.data.year-form.start.data.year)*12
            months = form.end.data.month-form.start.data.month
            if (form.end.data.day-form.start.data.day) < 0:
                months -= 1
            total_months = years + months
            if current_user.current_balance < total_months*amount:
                raise ValidationError('You do not have enough funds to make this pledge')
        else:
            raise ValidationError('Something went wrong with the selection, please try again or try choosing another frequency')
        
