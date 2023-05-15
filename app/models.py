from app import db
from flask import current_app
from flask_login import UserMixin, current_user
from sqlalchemy import String, Integer, Column, Boolean, ForeignKey, DateTime, Time, Float
from datetime import datetime, timezone
import time


class Donor(db.Model, UserMixin):
    id              = Column(Integer, primary_key=True)
    first_name      = Column(String(64), nullable=False)
    last_name       = Column(String(64), nullable=False)
    address         = Column(String(64), nullable=False)
    zip_code        = Column(String(20), nullable=False)
    phone_home      = Column(String(64))
    phone_cell      = Column(String(64), nullable=False, unique=True)
    email           = Column(String(64), nullable=False, unique=True)
    password        = Column(String(64), nullable=False)
    bank            = Column(String(64))
    account_number  = Column(String(64))
    name_on_account = Column(String(64))
    balance         = Column(Float, default=0)
    auto_replenish  = Column(Boolean, default=False)
    daily_pledges   = Column(Float, default=0)
    admin           = Column(Boolean, default=False)
    receipts        = db.relationship('Receipt', backref='donor', lazy='dynamic')
    pledges         = db.relationship('Pledge', backref='donor', lazy='dynamic')
    donations       = db.relationship('Donation', backref='donor', lazy='dynamic')


class Charity(db.Model, UserMixin):
    id               = Column(Integer, primary_key=True, autoincrement=False, unique=True)
    charity_name     = Column(String(64), nullable=False)
    address          = Column(String(64), nullable=False)
    zip_code         = Column(String(64), nullable=False)
    phone            = Column(String(64), nullable=False)
    website          = Column(String(64))
    email            = Column(String(64), nullable=False, unique=True)
    password         = Column(String(64), nullable=False)
    contact_name     = Column(String(64))
    contact_cell     = Column(String(64), unique=True)
    contact_position = Column(String(64))
    bank             = Column(String(64), nullable=False)
    account_number   = Column(String(64), nullable=False)
    balance          = Column(Float, default=0)
    authenticated    = Column(Boolean, default=False)
    receipts         = db.relationship('Receipt', backref='charity', lazy='dynamic')
    pledges         = db.relationship('Pledge', backref='charity', lazy='dynamic')
    donations       = db.relationship('Donation', backref='charity', lazy='dynamic')


class Receipt(db.Model):
    id         = Column(Integer, primary_key=True)
    amount     = Column(Integer, nullable=False)
    date       = Column(DateTime, nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))
    charity_id = Column(Integer, ForeignKey('charity.id'))


class Pledge(db.Model):
    id         = Column(Integer, primary_key=True)
    frequency  = Column(String, nullable=False)
    start_date = Column(DateTime)
    end_date   = Column(DateTime)
    amount     = Column(Integer, nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))
    charity_id = Column(Integer, ForeignKey('charity.id'))

    def process_pledge(self):
        db.session.add(self)
        db.session.commit()


class Donation(db.Model):
    id         = Column(Integer, primary_key=True)
    amount     = Column(Float, nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))
    charity_id = Column(Integer, ForeignKey('charity.id'))

    def process_donation(self):
        self.donor.balance -= self.amount
        self.charity.balance += self.amount
        db.session.add(self)
        db.session.commit()





# while True:
#     current_time = datetime.now().timestamp().__floor__()
#     time.sleep(1)
#     if current_time == datetime.max:
#         break


# current_pledges = []

        # frequency = self.frequency
        # start = self.start_date.timestamp().__floor__()
        # end = self.end_date.timestamp().__floor__()
        # now = datetime.now().timestamp().__floor__()
        # while now < end:
        #     if start <= now :
        #         if frequency == 'Month':
        #             self.donor.balance -= self.amount
        #             self.charity.balance += self.amount
        #             db.session.commit()
        #             self.start_date.year
        #             time.sleep(1)
        #             now = datetime.now().timestamp().__floor__()
        #             continue
        #         else:
        #             print(times.get(frequency))
        #             self.donor.balance -= self.amount
        #             self.charity.balance += self.amount
        #             db.session.commit()
        #             time.sleep(times.get(frequency))
        #             now = datetime.now().timestamp().__floor__()
        #             continue
        #     time.sleep(1)
        #     now = datetime.now().timestamp().__floor__()



                # if frequency == 'Second':
                #     self.donor.balance -= self.amount
                #     self.charity.balance += self.amount
                #     time.sleep(1)
                #     now = datetime.now().timestamp().__floor__()
                # elif frequency == 'Minute':
                #     self.donor.balance -= self.amount
                #     self.charity.balance += self.amount
                #     time.sleep(60)
                #     now = datetime.now().timestamp().__floor__()
                # elif frequency == 'Hour':
                #     self.donor.balance -= self.amount
                #     self.charity.balance += self.amount
                #     time.sleep(3600)
                #     now = datetime.now().timestamp().__floor__()
                # elif frequency == 'Day':
                #     self.donor.balance -= self.amount
                #     self.charity.balance += self.amount
                #     time.sleep(86400)
                #     now = datetime.now().timestamp().__floor__()
                # elif frequency == 'Week':
                #     self.donor.balance -= self.amount
                #     self.charity.balance += self.amount
                #     time.sleep(604800)
                #     now = datetime.now().timestamp().__floor__()

# elif frequency == 'Month':
#     years = (end_data.year-start_data.year)*12
#     months = end_data.month-start_data.month
#     if (end_data.day-start_data.day) < 0 or \
#     (end_data.day-start_data.day) == 0 and end_data.time() < start_data.time():
#         months -= 1
#     total_months = years + months
#     if total_months <= 0 or\
#         total_months == 1 and start_data.day > end_data.day or\
#         total_months == 1 and start_data.day == end_data.day and start_data.time() > end_data.time():
#         raise ValidationError('You must choose start and end dates that are at least a month apart')