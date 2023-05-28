from app.donor import donor
from flask import render_template, redirect, flash, url_for
from app.models import Donor, Charity
from flask_login import current_user, login_required
from app.donor.forms import AddAdmin, RemoveAdmin, AddFunds, UpdateDonorInfoForm
from app import db
from datetime import datetime
import pytz


@donor.route('/donor_profile/<donor_id>')
@login_required
def donor_profile_page(donor_id):
    is_donor = isinstance(current_user, Donor)
    if not is_donor:
        return redirect(url_for('organization.charity_profile_page', charity_id=current_user.id))
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    active_donor_pledges = []
    now = datetime.now(tz=pytz.timezone('Israel'))
    for pledge in donor.pledges:
        if pledge.end_date > now > pledge.start_date:
            pledge.start_date = pledge.start_date.astimezone(tz=pytz.timezone('Israel'))
            pledge.end_date = pledge.end_date.astimezone(tz=pytz.timezone('Israel'))
            active_donor_pledges.append(pledge)
    return render_template('profile.html',
                           donor=donor,
                           active_donor_pledges=active_donor_pledges)

@donor.route('/donor_profile/<donor_id>/scheduled_donor_pledges')
@login_required
def scheduled_donor_pledges(donor_id):
    is_donor = isinstance(current_user, Donor)
    if not is_donor:
        return redirect(url_for('organization.charity_profile_page', charity_id=current_user.id))
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    now = datetime.now(tz=pytz.timezone('Israel'))
    scheduled_donor_pledges = []
    for pledge in donor.pledges:
        if now < pledge.start_date:
            pledge.start_date = pledge.start_date.astimezone(tz=pytz.timezone('Israel'))
            pledge.end_date = pledge.end_date.astimezone(tz=pytz.timezone('Israel'))
            scheduled_donor_pledges.append(pledge)
    return render_template('scheduled_donor_pledges.html',
                           donor=donor,
                           scheduled_donor_pledges=scheduled_donor_pledges)

@donor.route('/donor_profile/<donor_id>/completed_donor_pledges')
@login_required
def completed_donor_pledges(donor_id):
    is_donor = isinstance(current_user, Donor)
    if not is_donor:
        return redirect(url_for('organization.charity_profile_page', charity_id=current_user.id))
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    now = datetime.now(tz=pytz.timezone('Israel'))
    completed_donor_pledges = []
    for pledge in donor.pledges:
        if now > pledge.start_date:
            pledge.start_date = pledge.start_date.astimezone(tz=pytz.timezone('Israel'))
            pledge.end_date = pledge.end_date.astimezone(tz=pytz.timezone('Israel'))
            completed_donor_pledges.append(pledge)
    return render_template('completed_donor_pledges.html',
                           donor=donor,
                           completed_donor_pledges=completed_donor_pledges)

@donor.route('/donor_profile/<donor_id>/all_one_time_donations')
@login_required
def all_one_time_donations(donor_id):
    is_donor = isinstance(current_user, Donor)
    if not is_donor:
        return redirect(url_for('organization.charity_profile_page', charity_id=current_user.id))
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    all_one_time_donations = donor.donations.all()
    return render_template('all_one_time_donations.html',
                           donor=donor,
                           all_one_time_donations=all_one_time_donations)

@donor.route('/donor_profile/<donor_id>/all_receipts')
@login_required
def all_receipts(donor_id):
    is_donor = isinstance(current_user, Donor)
    if not is_donor:
        return redirect(url_for('organization.charity_profile_page', charity_id=current_user.id))
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    all_receipts = donor.receipts.all()
    print(all_receipts)
    return render_template('all_receipts.html',
                           donor=donor,
                           all_receipts=all_receipts)



@donor.route('/profile/<donor_id>/add_funds', methods=('GET', 'POST'))
@login_required
def add_funds(donor_id):
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    add_funds_form = AddFunds()
    if add_funds_form.validate_on_submit():
        donor.balance += float(add_funds_form.amount.data)
        db.session.commit()
        flash('Funds added!', 'good')
        return redirect(url_for('donor.donor_profile_page', donor_id=current_user.id))
    return render_template('add_funds.html',
                           donor=donor,
                           add_funds_form=add_funds_form)



@donor.route('/profile/<donor_id>/edit_donor_profile', methods=('GET', 'POST'))
def edit_donor_profile(donor_id):
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    update_form = UpdateDonorInfoForm()
    if update_form.validate_on_submit():
        donor.first_name = update_form.first_name.data
        donor.last_name = update_form.last_name.data
        donor.address = update_form.address.data
        donor.zip_code = update_form.zip_code.data
        donor.phone_home = update_form.phone_home.data
        donor.phone_cell = update_form.phone_cell.data
        donor.email = update_form.email.data
        db.session.commit()
        flash('Account has been updated!', 'good')
        return redirect(url_for('donor.donor_profile_page', donor_id=donor.id))
    return render_template('edit_donor_profile.html',
                           donor=donor,
                           update_form=update_form)


@donor.route('authenticate_charity', methods=('GET', 'POST'))
@login_required
def authenticate_charity():
    if current_user.admin == False:
        return redirect(url_for('main.home'))
    charities_to_be_confirmed = Charity.query.filter_by(authenticated=False).all()
    return render_template('authenticate_charity.html',
                           charities_to_be_confirmed=charities_to_be_confirmed)


@donor.route('/add_admin', methods=('GET', 'POST'))
@login_required
def add_admin():
    if not current_user.id == 1:
        return redirect(url_for('main.home'))
    add_admin_form = AddAdmin()
    if add_admin_form.validate_on_submit():
        user = Donor.query.filter_by(id=add_admin_form.id.data).first()
        user.admin = True
        db.session.commit() 
        flash('Admin priviliges added to user')
        return redirect(url_for('donor.donor_profile_page', donor_id=current_user.id))
    return render_template('add_admin.html',
                           add_admin_form=add_admin_form)


@donor.route('/remove_admin', methods=('GET', 'POST'))
@login_required
def remove_admin():
    if not current_user.id == 1:
        return redirect(url_for('main.home'))
    main_admin = Donor.query.filter_by(id=1).first()
    remove_admin_form = RemoveAdmin()
    admins = Donor.query.filter_by(admin=True).all()
    remove_admin_form.admin.choices = [user.email for user in admins]
    remove_admin_form.admin.choices.remove(main_admin.email)
    if remove_admin_form.validate_on_submit():
        user = Donor.query.filter_by(email=remove_admin_form.admin.data).first()
        user.admin = False
        db.session.commit()
        flash('Admin priviliges removed from user')
        return redirect(url_for('donor.donor_profile_page', donor_id=current_user.id))
    return render_template('remove_admin.html',
                           remove_admin_form=remove_admin_form)
