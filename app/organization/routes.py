from app.organization import organization
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Charity, Donor, Pledge, Donation
from app import db, scheduler
from app.organization.forms import RecurringDonationForm, SingleDonationForm, UpdateCharityInfoForm
from app.organization.utils import pledge_start_date, pledge_transaction
from app.main.forms import CharityAuthenticateForm
from datetime import datetime




@organization.route('/edit_charity_profile/<charity_id>', methods=('GET', 'POST'))
@login_required
def edit_charity_profile(charity_id):
    if not int(current_user.id) == int(charity_id):
        return redirect(url_for('main.home'))
    charity = Charity.query.filter_by(id=charity_id).first()
    update_form = UpdateCharityInfoForm()
    if update_form.validate_on_submit():
        charity.id = update_form.id.data
        charity.charity_name = update_form.charity_name.data
        charity.address = update_form.address.data
        charity.zip_code = update_form.zip_code.data
        charity.phone = update_form.phone.data
        charity.website = update_form.website.data
        charity.email = update_form.email.data
        charity.contact_name = update_form.contact_name.data
        charity.contact_cell = update_form.contact_cell.data
        charity.contact_position = update_form.contact_position.data
        charity.bank = update_form.bank.data
        charity.account_number = update_form.account_number.data
        db.session.commit()
        flash('Account has been updated!', 'good')
        return redirect(url_for('organization.charity_profile_page', charity_id=charity.id))
    return render_template('edit_charity_profile.html',
                           charity=charity,
                           update_form=update_form)


@organization.route('/charity_profile/<charity_id>', methods=('GET', 'POST'))
@login_required
def charity_profile_page(charity_id):
    is_charity = isinstance(current_user, Charity)
    if not is_charity:
        return redirect(url_for('donor.donor_profile_page', donor_id=current_user.id))
    if not int(current_user.id) == int(charity_id):
        return redirect(url_for('main.home'))
    charity = Charity.query.filter_by(id=charity_id).first()
    return render_template('charity_profile_page.html',
                           charity=charity)

@organization.route('/authentication_details/<charity_id>', methods=('GET', 'POST'))
@login_required
def authentication_details(charity_id):
    if current_user.admin == False:
        return redirect(url_for('main.home'))
    update_form = CharityAuthenticateForm()
    charity = Charity.query.filter_by(id=charity_id).first()
    if update_form.validate_on_submit():
        check_id = Charity.query.filter_by(id=update_form.id.data).first()
        if check_id and not check_id.id == charity.id:
            flash('A Charity with this ID exists already, please check your info', 'bad')
            return redirect(url_for('organization.authentication_details',
                                    charity_id=charity.id))
        
        check_email = Charity.query.filter_by(email=update_form.email.data).first()
        if check_email and not check_email.email == charity.email:
            flash('A Charity with this email exists already, please check your info', 'bad')
            return redirect(url_for('organization.authentication_details',
                                    charity_id=charity.id))

        charity.id = update_form.id.data
        charity.charity_name = update_form.charity_name.data
        charity.address = update_form.address.data
        charity.zip_code = update_form.zip_code.data
        charity.phone = update_form.phone.data
        charity.website = update_form.website.data
        charity.email = update_form.email.data
        charity.contact_name = update_form.contact_name.data
        charity.contact_cell = update_form.contact_cell.data
        charity.contact_position = update_form.contact_position.data
        charity.bank = update_form.bank.data
        charity.account_number = update_form.account_number.data
        charity.authenticated = True
        db.session.commit()
        flash('Charity has been authenticated!', 'good')
        return redirect(url_for('donor.authenticate_charity'))

    return render_template('authentication_details.html',
                           charity=charity,
                           update_form=update_form)

@organization.route('/delete_request/<charity_id>', methods=('GET', 'POST'))
def delete_request(charity_id):
    if current_user.admin == False:
        return redirect(url_for('main.home'))
    charity = Charity.query.filter_by(id=charity_id).first()
    db.session.delete(charity)
    db.session.commit()
    flash('Request has been deleted')
    return redirect(url_for('donor.authenticate_charity'))


@organization.route('/recurring_donation/charity/<charity_id>', methods=('GET', 'POST'))
@login_required
def recurring_donation_page(charity_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=current_user.id).first()
    rd_form = RecurringDonationForm()
    if rd_form.validate_on_submit():
        dt_start = rd_form.start.data
        dt_end = rd_form.end.data
        pledge = Pledge(
            frequency=rd_form.how_often.data,
            start_date=dt_start,
            end_date=dt_end,
            amount=float(rd_form.amount.data),
            donor=donor,
            charity=charity
        )
        pledge.process_pledge()
        return redirect(url_for('organization.processing_recurring_donations', charity_id=charity.id, donor_id=donor.id, pledge_id=pledge.id))
    return render_template('recurring_donation_page.html',
                           charity=charity,
                           donor=donor,
                           rd_form=rd_form)


@organization.route('/processing_recurring_donations/charity/<charity_id>/donor/<donor_id>/pledge/<pledge_id>', methods=('GET', 'POST'))
@login_required
def processing_recurring_donations(charity_id, donor_id, pledge_id):
    if not current_user.id == int(donor_id):
        return redirect(url_for('main.home'))
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=donor_id).first()
    pledge = Pledge.query.filter_by(id=pledge_id).first()
    scheduler.add_job(id=pledge_id, func=pledge_start_date, args=(pledge.id, ), trigger='date', run_date=pledge.start_date)
    return redirect(url_for('organization.recurring_donation_page', charity_id=charity.id, donor_id=donor.id))


@organization.route('/one_time_donation/charity/<charity_id>', methods=('GET', 'POST'))
@login_required
def one_time_donation_page(charity_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=current_user.id).first()
    sd_form = SingleDonationForm()
    if sd_form.validate_on_submit():
        donation = Donation(
            amount=float(sd_form.amount.data),
            donor=donor,
            charity=charity
        )
        donation.process_donation()
        flash('Donation made succesfully!')
        return redirect(url_for('organization.one_time_donation_page', charity_id=charity.id, donor_id=donor.id))
    return render_template('one_time_donation_page.html',
                           charity=charity,
                           donor=donor,
                           sd_form=sd_form)


@organization.route('/charity_info_page/<charity_id>')
def charity_info_page(charity_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    return render_template('charity_info_page.html',
                           charity=charity)

@organization.route('/all_charities')
def all_charities():
    is_charity = isinstance(current_user, Charity)
    if is_charity:
        return redirect(url_for('main.home'))
    charities = Charity.query.filter_by(authenticated=True).all()
    return render_template('all_charities.html',
                           charities=charities,
                           is_charity=is_charity)





