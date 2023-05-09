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



