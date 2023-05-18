from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from app.models import Donor

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
    submit = SubmitField('Add Funds')