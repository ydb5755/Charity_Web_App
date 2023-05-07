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
    password        = Column(String(64), nullable=False)
    bank            = Column(String(64))
    account_number  = Column(String(64))
    name_on_account = Column(String(64))
    current_balance = Column(Integer, default=0)
    auto_replenish  = Column(Boolean, default=False)
    daily_pledges   = Column(Integer, default=0)
    receipts        = db.relationship('Receipt', backref='donor', lazy='dynamic')
    pledges         = db.relationship('Pledge', backref='donor', lazy='dynamic')

class Admin(Donor, db.Model, UserMixin):
    charities_to_confirm = db.relationship('Charity', backref='admin', lazy='dynamic')

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
    balance          = Column(Integer, default=0)
    authenticated    = Column(Boolean, default=False)
    admin_id         = Column(Integer, ForeignKey('admin.id'))
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