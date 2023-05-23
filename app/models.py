from app import db
from flask import current_app
from flask_login import UserMixin, current_user
from sqlalchemy import String, Integer, Column, Boolean, ForeignKey, DateTime, Time, Float, Text, TIMESTAMP
from datetime import datetime, timezone, timedelta
import jwt


class Donor(db.Model, UserMixin):
    id              = Column(Integer, primary_key=True)
    first_name      = Column(String(64), nullable=False)
    last_name       = Column(String(64), nullable=False)
    address         = Column(String(64), nullable=False)
    zip_code        = Column(String(20), nullable=False)
    phone_home      = Column(String(64))
    phone_cell      = Column(String(64), nullable=False, unique=True)
    email           = Column(String(64), nullable=False, unique=True)
    password        = Column(String(200), nullable=False)
    bank            = Column(String(64))
    account_number  = Column(String(64))
    name_on_account = Column(String(64))
    balance         = Column(Float(4), default=0)
    auto_replenish  = Column(Boolean, default=False)
    daily_pledges   = Column(Float, default=0)
    admin           = Column(Boolean, default=False)
    receipts        = db.relationship('Receipt', backref='donor', lazy='dynamic')
    pledges         = db.relationship('Pledge', backref='donor', lazy='dynamic')
    donations       = db.relationship('Donation', backref='donor', lazy='dynamic')

    
    def get_reset_token(self, expiration=600):
        reset_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.now(tz=timezone.utc)
                       + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    
    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        if not Donor.query.get(data.get('confirm')):
            return None
        return Donor.query.get(data.get('confirm'))


class Charity(db.Model, UserMixin):
    id               = Column(Integer, primary_key=True, autoincrement=False, unique=True)
    charity_name     = Column(String(64), nullable=False)
    address          = Column(String(64), nullable=False)
    zip_code         = Column(String(64), nullable=False)
    phone            = Column(String(64), nullable=False)
    website          = Column(String(64))
    email            = Column(String(64), nullable=False, unique=True)
    password         = Column(String(200), nullable=False)
    contact_name     = Column(String(64))
    contact_cell     = Column(String(64), unique=True)
    contact_position = Column(String(64))
    bank             = Column(String(64), nullable=False)
    account_number   = Column(String(64), nullable=False)
    balance          = Column(Float(4), default=0)
    home_page_text   = Column(String(200), default='')
    description      = Column(Text, default='')
    authenticated    = Column(Boolean, default=False)
    receipts         = db.relationship('Receipt', backref='charity', lazy='dynamic')
    pledges         = db.relationship('Pledge', backref='charity', lazy='dynamic')
    donations       = db.relationship('Donation', backref='charity', lazy='dynamic')


    def get_reset_token(self, expiration=600):
        reset_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.now(tz=timezone.utc)
                       + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    
    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        if not Charity.query.get(data.get('confirm')):
            return None
        return Charity.query.get(data.get('confirm'))


class Receipt(db.Model):
    id         = Column(Integer, primary_key=True)
    amount     = Column(Integer, nullable=False)
    date       = Column(DateTime, nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))
    charity_id = Column(Integer, ForeignKey('charity.id'))


class Pledge(db.Model):
    id         = Column(Integer, primary_key=True)
    frequency  = Column(String, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date   = Column(TIMESTAMP(timezone=True))
    amount     = Column(Float(4), nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))
    charity_id = Column(Integer, ForeignKey('charity.id'))

    def process_pledge(self):
        db.session.add(self)
        db.session.commit()


class Donation(db.Model):
    id         = Column(Integer, primary_key=True)
    amount     = Column(Float(4), nullable=False)
    donor_id   = Column(Integer, ForeignKey('donor.id'))
    charity_id = Column(Integer, ForeignKey('charity.id'))

    def process_donation(self):
        self.donor.balance -= float(self.amount)
        self.charity.balance += float(self.amount)
        db.session.add(self)
        db.session.commit()


