from app import scheduler, db, apschedule
from app.models import Pledge
from datetime import datetime


def pledge_transaction(pledge_id):
    with apschedule.app.app_context():
        pledge = Pledge.query.filter_by(id=pledge_id).first()
        pledge.donor.balance -= pledge.amount
        pledge.donor.balance = round(pledge.donor.balance, 2)
        pledge.charity.balance += pledge.amount
        pledge.charity.balance = round(pledge.charity.balance, 2)
        db.session.commit()



times = {
    'Minute':60,
    'Hour':3600,
    'Day':86400,
    'Week':604800
}