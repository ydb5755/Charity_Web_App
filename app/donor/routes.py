from app.donor import donor
from flask import render_template, redirect, flash, url_for
from app.models import Donor, Charity
from flask_login import current_user, login_required
from app.donor.forms import AddAdmin, RemoveAdmin, AddFunds
from app import db


@donor.route('/profile/<donor_id>', methods=('GET', 'POST'))
@login_required
def profile_page(donor_id):
    if not int(current_user.id) == int(donor_id):
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    charities_to_be_confirmed = Charity.query.filter_by(authenticated=False)
    add_funds_form = AddFunds()
    if add_funds_form.validate_on_submit():
        donor.current_balance += add_funds_form.amount.data
        db.session.commit()
        flash('Funds added!')
        return redirect(url_for('donor.profile_page', donor_id=current_user.id))
    return render_template('profile.html',
                           donor=donor,
                           charities_to_be_confirmed=charities_to_be_confirmed,
                           add_funds_form=add_funds_form)

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
    remove_admin_form = RemoveAdmin()
    admins = Donor.query.filter_by(admin=True).all()
    print(admins)
    remove_admin_form.admin.choices = [user.email for user in admins]  #.remove(Donor.query.filter_by(id=1).first())
    if remove_admin_form.validate_on_submit():
        user = Donor.query.filter_by(email=remove_admin_form.admin.data).first()
        user.admin = False
        db.session.commit()
        flash('Admin priviliges removed from user')
        return redirect(url_for('donor.profile_page', donor_id=current_user.id))
    return render_template('remove_admin.html',
                           remove_admin_form=remove_admin_form)
