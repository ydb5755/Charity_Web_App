from app.organization import organization
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Charity, Donor, Pledge, Donation
from app import db
from app.organization.forms import RecurringDonationForm, SingleDonationForm
from datetime import datetime, timezone




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

@organization.route('/donation_page/charity/<charity_id>/donor/<donor_id>')
@login_required
def donation_page(charity_id, donor_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=donor_id).first()
    return render_template('donation_page.html',
                           charity=charity,
                           donor=donor)


@organization.route('/recurring_donation/charity/<charity_id>/donor/<donor_id>', methods=('GET', 'POST'))
@login_required
def recurring_donation_page(charity_id, donor_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=donor_id).first()
    rd_form = RecurringDonationForm()
    if rd_form.validate_on_submit():
        dt_start = rd_form.start.data.timestamp()
        dt_end = rd_form.end.data.timestamp()
        # pledge = Pledge(
        #     frequency=rd_form.how_often.data,
        #     start_date=datetime(dt_start),
        #     end_date=datetime(dt_end),
        #     amount=rd_form.amount.data,
        #     donor=donor,
        #     charity=charity
        # )
        # pledge.process_pledge()
        print(dt_start)
        return redirect(url_for('organization.donation_page', charity_id=charity.id, donor_id=donor.id))
    print(rd_form.errors)
    return render_template('recurring_donation_page.html',
                           charity=charity,
                           donor=donor,
                           rd_form=rd_form)


@organization.route('/one_time_donation/charity/<charity_id>/donor/<donor_id>', methods=('GET', 'POST'))
@login_required
def one_time_donation_page(charity_id, donor_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=donor_id).first()
    sd_form = SingleDonationForm()
    if sd_form.validate_on_submit():
        donation = Donation(
            amount=sd_form.amount.data,
            donor=donor,
            charity=charity
        )
        donation.process_donation()
        return redirect(url_for('organization.donation_page', charity_id=charity.id, donor_id=donor.id))
    return render_template('one_time_donation_page.html',
                           charity=charity,
                           donor=donor,
                           sd_form=sd_form)