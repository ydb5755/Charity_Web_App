from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from app.models import Donor

class AddAdmin(FlaskForm):
    id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Add Admin')

    def validate_id(form, field):
        donor = Donor.query.filter_by(id=field.data).first()
        if not donor:
            raise ValidationError('This user does not exist, try another id')
        if donor.admin == True:
            raise ValidationError('This user is already an admin')
        

class RemoveAdmin(FlaskForm):
    admin = SelectField('Select Admin to remove priviliges', validators=[DataRequired()])
    submit = SubmitField('Remove Admin')

class AddFunds(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Funds')