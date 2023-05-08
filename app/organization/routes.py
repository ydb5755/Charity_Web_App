from app.organization import organization
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Charity, Donor
from app import db
from app.organization.forms import RecurringDonationForm, SingleDonationForm




@organization.route('/charity_page/<charity_id>')
@login_required
def charity_page(charity_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    return render_template('charity_page.html',
                           charity=charity)

@organization.route('/authenticate_charity/<charity_id>', methods=('GET', 'POST'))
@login_required
def authenticate(charity_id):
    if current_user.admin == False:
        return redirect(url_for('main.home'))
    charity = Charity.query.filter_by(id=charity_id).first()
    charity.authenticated = True
    db.session.commit()
    flash('Charity has been authenticated!')
    return redirect(url_for('donor.profile_page', donor_id=current_user.id))

@organization.route('/donation_page/<charity_id>/<donor_id>')
@login_required
def donation_page(charity_id, donor_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=donor_id).first()
    rd_form = RecurringDonationForm()
    if rd_form.validate_on_submit():
        pass

    sd_form = SingleDonationForm()
    if sd_form.validate_on_submit():
        pass

    return render_template('donation_page.html',
                           charity=charity,
                           donor=donor,
                           rd_form=rd_form,
                           sd_form=sd_form)