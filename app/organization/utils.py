from app import scheduler, db
from app.models import Pledge
from datetime import datetime


def pledge_transaction(pledge_id):
    with scheduler.app.app_context():
        pledge = Pledge.query.filter_by(id=pledge_id).first()
        if datetime.now() > pledge.end_date:
            return scheduler.remove_job(str(pledge.id))
        if datetime.now() > pledge.start_date:
            pledge.donor.balance -= pledge.amount
            pledge.charity.balance += pledge.amount
            db.session.commit()


def pledge_start_date(pledge_id):
    with scheduler.app.app_context():
        pledge = Pledge.query.filter_by(id=pledge_id).first()
        frequency = pledge.frequency
        if frequency == 'Month':
            scheduler.add_job(id=str(pledge_id), func=pledge_transaction, args=(pledge.id, ), trigger='cron', day=25, hour=12)
        else:
            scheduler.add_job(id=str(pledge_id), func=pledge_transaction, args=(pledge.id, ), trigger='interval', seconds=times.get(frequency))

times = {
    'Second':1,
    'Minute':60,
    'Hour':3600,
    'Day':86400,
    'Week':604800
}