from app.donor import donor
from flask import render_template, redirect, flash, url_for
from app.models import Donor, Charity
from flask_login import current_user, login_required
from app.donor.forms import AddAdmin, RemoveAdmin, AddFunds, UpdateDonorInfoForm
from app import db
from werkzeug.security import generate_password_hash


@donor.route('/profile/<donor_id>', methods=('GET', 'POST'))
@login_required
def profile_page(donor_id):
    is_donor = isinstance(current_user, Donor)
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    add_funds_form = AddFunds()
    if add_funds_form.validate_on_submit():
        donor.balance += float(add_funds_form.amount.data)
        db.session.commit()
        flash('Funds added!')
        return redirect(url_for('donor.profile_page', donor_id=current_user.id))
    return render_template('profile.html',
                           donor=donor,
                           add_funds_form=add_funds_form,
                           is_donor=is_donor)


@donor.route('/profile/<donor_id>/edit_donor_profile', methods=('GET', 'POST'))
def edit_donor_profile(donor_id):
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
        # if update_form.password.data:
        #     if update_form.password.data != update_form.confirm_password.data:
        #         flash('If you want to update your password then it must match the confirm password field', 'bad')
        #         return redirect(url_for('edit_donor_profile', donor_id=donor.id))
        #     donor.password = update_form.password.data
        db.session.commit()
        flash('Account has been updated!', 'good')
        return redirect(url_for('donor.profile_page', donor_id=donor.id))
    return render_template('edit_donor_profile.html',
                           donor=donor,
                           update_form=update_form)


@donor.route('authenticate_charity', methods=('GET', 'POST'))
@login_required
def authenticate_charity():
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
        return redirect(url_for('donor.profile_page', donor_id=current_user.id))
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
        return redirect(url_for('donor.profile_page', donor_id=current_user.id))
    return render_template('remove_admin.html',
                           remove_admin_form=remove_admin_form)
