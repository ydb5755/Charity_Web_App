from app.main import main
from flask import render_template, url_for, redirect, flash, session
from app.models import Charity, Donor
from app.main.forms import LoginForm
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import login_manager

@main.route('/')
def home():
    all_charities = Charity.query.all()
    return render_template('home.html', 
                           all_charities=all_charities)

@main.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.type_of_user == 'Donor':
            donor = Donor.query.filter_by(email=form.email.data).first()
            if not donor or not check_password_hash(donor.password, form.password.data):
                flash('Please check your login details and try again.')
                return redirect(url_for('main.login'))
            session['account_type'] = 'Donor'
            login_user(donor, remember=form.remember.data)
        if form.type_of_user == 'Charity':
            charity = Charity.query.filter_by(email=form.email.data).first()
            if not charity or not check_password_hash(charity.password, form.password.data):
                flash('Please check your login details and try again.')
                return redirect(url_for('main.login'))
            session['account_type'] = 'Charity'
            login_user(charity, remember=form.remember.data)
        
        
        flash("You've been logged in successfully!")
        return redirect(url_for('main.home'))
    return render_template('login.html')