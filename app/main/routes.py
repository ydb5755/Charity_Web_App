from app.main import main
from flask import render_template, url_for, redirect, flash, session, request
from app.models import Charity, Donor
from app.main.forms import LoginForm, DonorSignUpForm, CharitySignUpForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from random import randint

is_charity = isinstance(current_user, Charity)

@main.route('/')
def home():
    all_charities = Charity.query.filter_by(authenticated=True).all()
    five_charities = []
    for _ in range(5):
        five_charities.append(all_charities[randint(0, (len(all_charities) - 1))])
    return render_template('home.html', 
                           all_charities=all_charities,
                           five_charities=five_charities)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/login_donor', methods=('GET', 'POST'))
def login_donor():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        donor = Donor.query.filter_by(email=form.email.data).first()
        if not donor or not check_password_hash(donor.password, form.password.data):
            flash('Please check your login details and try again.', 'bad')
            return redirect(url_for('main.login_donor'))
        login_user(donor, remember=form.remember.data)
        flash("You've been logged in successfully!", 'good')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('login_donor.html', form=form)


@main.route('/login_charity', methods=('GET', 'POST'))
def login_charity():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        charity = Charity.query.filter_by(email=form.email.data).first()
        if not charity or not check_password_hash(charity.password, form.password.data):
            flash('Please check your login details and try again.', 'bad')
            return redirect(url_for('main.login_charity'))
        if charity.authenticated == False:
            flash('Your charity has not been confirmed yet, you will have to wait to login', 'bad')
            return redirect(url_for('main.home'))
        login_user(charity, remember=form.remember.data)
        flash("You've been logged in successfully!", 'good')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('login_charity.html', form=form)


@main.route('/signup_donor', methods=('GET', 'POST'))
def signup_donor():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    donor_form = DonorSignUpForm()
    if donor_form.validate_on_submit():
        if Donor.query.filter_by(email=donor_form.email.data).first():
            flash('This email is already signed up, please try another email or try to log in using this email', 'bad')
            return redirect(url_for('main.signup'))
        if donor_form.password.data != donor_form.confirm_password.data:
            flash('Passwords do not match, please try again', 'bad')
            return redirect(url_for('main.signup'))
        pw = generate_password_hash(donor_form.password.data, method='scrypt')
        donor = Donor(
                    first_name=donor_form.first_name.data,
                    last_name=donor_form.last_name.data,
                    address=donor_form.address.data,
                    zip_code=donor_form.zip_code.data,
                    phone_home=donor_form.phone_home.data,
                    phone_cell=donor_form.phone_cell.data,
                    email=donor_form.email.data,
                    password=pw
        )
        db.session.add(donor)
        db.session.commit()
        flash("You've succesffully signed up! Please log in to continue!", 'good')
        return redirect(url_for('main.login_donor'))
    return render_template('signup_donor.html', 
                           donor_form=donor_form)

@main.route('/signup_charity', methods=('GET', 'POST'))
def signup_charity():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    charity_form = CharitySignUpForm()
    if charity_form.validate_on_submit():
        if Charity.query.filter_by(id=charity_form.id.data).first():
            flash('A charity with this id already exists with us. Either check your id or try logging in.', 'bad')
            return redirect(url_for('main.signup'))
        charity = Charity(
                        id = charity_form.id.data,
                        charity_name = charity_form.charity_name.data,
                        address = charity_form.address.data,
                        zip_code = charity_form.zip_code.data,
                        phone = charity_form.phone.data,
                        website = charity_form.website.data,
                        email = charity_form.email.data,
                        contact_name = charity_form.contact_name.data,
                        contact_cell = charity_form.contact_cell.data,
                        contact_position = charity_form.contact_position.data,
                        bank = charity_form.bank.data,
                        account_number = charity_form.account_number.data
        )
        db.session.add(charity)
        db.session.commit()
        flash('Your charity has been submitted for review! One of our staff will reach out to you in the next couple of business days to confirm details and activate your account.', 'good')
        return redirect(url_for('main.home'))
    return render_template('signup_charity.html',
                           charity_form=charity_form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out!", 'good')
    return redirect(url_for('main.home'))