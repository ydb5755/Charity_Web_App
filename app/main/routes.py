from app.main import main
from flask import render_template, url_for, redirect, flash, session, request
from app.models import Charity, Donor
from app.main.forms import LoginForm, DonorSignUpForm, CharitySignUpForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

is_charity = isinstance(current_user, Charity)

@main.route('/')
def home():
    all_charities = Charity.query.all()
    return render_template('home.html', 
                           all_charities=all_charities)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.type_of_user.data == 'Donor':
            donor = Donor.query.filter_by(email=form.email.data).first()
            if not donor or not check_password_hash(donor.password, form.password.data):
                flash('Please check your login details and try again.')
                return redirect(url_for('main.login'))
            login_user(donor, remember=form.remember.data)
        if form.type_of_user.data == 'Charity':
            charity = Charity.query.filter_by(email=form.email.data).first()
            if not charity or not check_password_hash(charity.password, form.password.data):
                flash('Please check your login details and try again.')
                return redirect(url_for('main.login'))
            if charity.authenticated == False:
                flash('Your charity has not been confirmed yet, you will have to wait to login')
                return redirect(url_for('main.home'))
            login_user(charity, remember=form.remember.data)
        flash("You've been logged in successfully!")
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('login.html', form=form)

@main.route('/signup', methods=('GET', 'POST'))
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    donor_form = DonorSignUpForm()
    if donor_form.validate_on_submit():
        if Donor.query.filter_by(email=donor_form.email.data).first():
            flash('This email is already signed up, please try another email or try to log in using this email')
            return redirect(url_for('main.signup'))
        if donor_form.password.data != donor_form.confirm_password.data:
            flash('Passwords do not match, please try again')
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
        flash("You've succesffully signed up! Please log in to continue!")
        return redirect(url_for('main.login'))
    charity_form = CharitySignUpForm()
    if charity_form.validate_on_submit():
        if Charity.query.filter_by(id=charity_form.id.data).first():
            flash('A charity with this id already exists with us. Either check your id or try logging in.')
            return redirect(url_for('main.signup'))
        if charity_form.password.data != charity_form.confirm_password.data:
            flash('Passwords do not match, please try again')
            return redirect(url_for('main.signup'))
        pw = generate_password_hash(charity_form.password.data, method='scrypt')
        charity = Charity(
                        id = charity_form.id.data,
                        charity_name = charity_form.charity_name.data,
                        address = charity_form.address.data,
                        zip_code = charity_form.zip_code.data,
                        phone = charity_form.phone.data,
                        website = charity_form.website.data,
                        email = charity_form.email.data,
                        password = pw,
                        contact_name = charity_form.contact_name.data,
                        contact_cell = charity_form.contact_cell.data,
                        contact_position = charity_form.contact_position.data,
                        bank = charity_form.bank.data,
                        account_number = charity_form.account_number.data,
        )
        db.session.add(charity)
        db.session.commit()
        flash('Your charity has been submitted for review! One of our staff will reach out to you in the next couple of business days to confirm details and activate your account.')
        return redirect(url_for('main.home'))
    return render_template('signup.html', 
                           donor_form=donor_form,
                           charity_form=charity_form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out!")
    return redirect(url_for('main.home'))