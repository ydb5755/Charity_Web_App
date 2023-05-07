from app import db
from flask_login import UserMixin
from sqlalchemy import String, Integer, Column, Boolean, ForeignKey, DateTime, Time


class Donor(db.Model, UserMixin):
    id              = Column(Integer, primary_key=True)
    first_name      = Column(String(64), nullable=False)
    last_name       = Column(String(64), nullable=False)
    address         = Column(String(64), nullable=False)
    zip_code        = Column(String(20), nullable=False)
    phone_home      = Column(String(64))
    phone_cell      = Column(String(64), nullable=False, unique=True)
    email           = Column(String(64), nullable=False, unique=True)
    bank            = Column(String(64), nullable=False)
    account_number  = Column(String(64), nullable=False)
    name_on_account = Column(String(64), nullable=False)
    current_balance = Column(Integer, default=0)
    auto_replenish  = Column(Boolean, default=False)
    daily_pledges   = Column(Integer, default=0)
    receipts        = db.relationship('Receipt', backref='donor', lazy='dynamic')
    pledges         = db.relationship('Pledge', backref='donor', lazy='dynamic')

class Charity(db.Model, UserMixin):
    id               = Column(Integer, primary_key=True, autoincrement=False)
    charity_name     = Column(String(64), nullable=False)
    address          = Column(String(64), nullable=False)
    zip_code         = Column(String(64), nullable=False)
    phone            = Column(String(64), nullable=False)
    website          = Column(String(64), nullable=False)
    email            = Column(String(64), nullable=False, unique=True)
    contact_name     = Column(String(64), nullable=False)
    contact_cell     = Column(String(64), nullable=False, unique=True)
    contact_position = Column(String(64), nullable=False)
    bank             = Column(String(64), nullable=False)
    account_number   = Column(String(64), nullable=False)
    balance          = Column(Integer, default=0)
    receipts         = db.relationship('Receipt', backref='charity', lazy='dynamic')




class Receipt(db.Model):
    id         = Column(Integer, primary_key=True)
    amount     = Column(Integer, nullable=False)
    date       = Column(DateTime, nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))
    charity_id = Column(Integer, ForeignKey('charity.id'))



class Pledge(db.Model):
    id         = Column(Integer, primary_key=True)
    frequency  = Column(Time, nullable=False)
    start_date = Column(DateTime)
    end_date   = Column(DateTime)
    amount     = Column(Integer, nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))