from flask_wtf import FlaskForm
from wtforms import StringField,\
                    EmailField,\
                    PasswordField,\
                    SubmitField,\
                    SelectField,\
                    BooleanField,\
                    DateTimeField
from wtforms.validators import DataRequired



class SingleDonationForm(FlaskForm):
    amount = StringField('How much would you like to donate?')
    submit = SubmitField('Donate')

class RecurringDonationForm(FlaskForm):
    amount = StringField('How much would you like to donate?')
    how_often = SelectField('How often would you like to make this payment?', choices=['Second', 'Minute', 'Hour', 'Day', 'Week', 'Month'])
    start = DateTimeField('When should the payments start?')
    end = DateTimeField('When would you like the payments to end?')
    submit = SubmitField('Donate')