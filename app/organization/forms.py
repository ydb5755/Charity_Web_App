from flask_wtf import FlaskForm
from wtforms import StringField,\
                    EmailField,\
                    PasswordField,\
                    SubmitField,\
                    SelectField,\
                    BooleanField,\
                    DateTimeField,\
                    DateField,\
                    TimeField
from wtforms.validators import DataRequired



class SingleDonationForm(FlaskForm):
    amount = StringField('How much would you like to donate?')
    submit = SubmitField('Donate')

class RecurringDonationForm(FlaskForm):
    amount = StringField('How much would you like to donate?')
    how_often = SelectField('How often would you like to make this payment?', choices=['Second', 'Minute', 'Hour', 'Day', 'Week', 'Month'])
    start = DateField('What date should the payments start?')
    start_time = TimeField('At what time should it start?')
    end = DateField('What date should the payments end?')
    end_time = TimeField('At what time should it end?')
    submit = SubmitField('Donate')