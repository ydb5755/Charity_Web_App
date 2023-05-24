from app.organization import organization
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Charity, Donor, Pledge, Donation
from app import db, scheduler
from app.organization.forms import RecurringDonationForm, SingleDonationForm, UpdateCharityInfoForm, ConfirmAmountForm
from app.organization.utils import pledge_transaction, times
from app.main.forms import CharityAuthenticateForm
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import pytz



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
        start = rd_form.start.data   
        end = rd_form.end.data
        frequency = rd_form.how_often.data
        amount=float(rd_form.amount.data)
        return redirect(url_for('organization.confirm_recurring_donation', 
                                charity_id=charity.id,
                                start=start,
                                end=end,
                                frequency=frequency,
                                amount=amount))
    return render_template('recurring_donation_page.html',
                           charity=charity,
                           donor=donor,
                           rd_form=rd_form)


@organization.route('/confirm_recurring_donation/<charity_id>/<start>/<end>/<frequency>/<amount>', methods=('GET', 'POST'))
@login_required
def confirm_recurring_donation(charity_id, start, end, frequency, amount):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=current_user.id).first()
    time_zone_start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S').astimezone(tz=pytz.timezone('Israel'))
    time_zone_end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S').astimezone(tz=pytz.timezone('Israel'))
    time_zone_start = time_zone_start.astimezone(tz=pytz.utc)
    time_zone_end = time_zone_end.astimezone(tz=pytz.utc)
    if frequency == 'Month':
        years = (time_zone_end.year-time_zone_start.year)*12
        months = time_zone_end.month-time_zone_start.month
        total = float(years + months) * float(amount)
    else:
        time_stamp_start = float(time_zone_start.timestamp())
        time_stamp_end = float(time_zone_end.timestamp())
        total = ((time_stamp_end - time_stamp_start) / times.get(frequency)) * float(amount)
    confirm_form = ConfirmAmountForm()
    if confirm_form.validate_on_submit():
        pledge = Pledge(
            frequency=frequency,
            start_date=time_zone_start,
            end_date=time_zone_end,
            amount=amount,
            donor=donor,
            charity=charity
        )
        pledge.process_pledge()
        return redirect(url_for('organization.processing_recurring_donations', charity_id=pledge.charity.id, donor_id=pledge.donor.id, pledge_id=pledge.id))
    return render_template('confirm_recurring_payment.html',
                           confirm_form=confirm_form,
                           total=total,
                           charity=charity)


@organization.route('/processing_recurring_donations/charity/<charity_id>/donor/<donor_id>/pledge/<pledge_id>', methods=('GET', 'POST'))
@login_required
def processing_recurring_donations(charity_id, donor_id, pledge_id):
    if not current_user.id == int(donor_id):
        return redirect(url_for('main.home'))
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=donor_id).first()
    pledge = Pledge.query.filter_by(id=pledge_id).first()
    frequency = pledge.frequency
    if frequency == 'Month':
        scheduler.add_job(id=str(pledge_id), 
                          func=pledge_transaction, 
                          args=[pledge.id], 
                          trigger=CronTrigger(day=25, 
                                              hour=12, 
                                              timezone=pytz.timezone('Israel')
                                              ),
                          misfire_grace_time=None, 
                          coalesce=False, 
                          max_instances=20)
    else:
        scheduler.add_job(id=str(pledge_id), 
                            func=pledge_transaction, 
                            args=[pledge.id], 
                            trigger=IntervalTrigger(seconds=times.get(frequency), 
                                                    start_date=pledge.start_date, 
                                                    end_date=pledge.end_date, 
                                                    timezone=pytz.timezone('Israel')
                                                    ), 
                            misfire_grace_time=None, 
                            coalesce=False, 
                            max_instances=20)
    flash('Recurring payment has been scheduled', 'good')
    return redirect(url_for('organization.recurring_donation_page', charity_id=charity.id, donor_id=donor.id))


@organization.route('/one_time_donation/charity/<charity_id>', methods=('GET', 'POST'))
@login_required
def one_time_donation_page(charity_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=current_user.id).first()
    sd_form = SingleDonationForm()
    if sd_form.validate_on_submit():
        amount=round(float(sd_form.amount.data), 2)
        donor=donor
        charity=charity
        return redirect(url_for('organization.confirm_one_time_donation', charity_id=charity.id, amount=amount))
    return render_template('one_time_donation_page.html',
                           charity=charity,
                           donor=donor,
                           sd_form=sd_form)


@organization.route('/confirm_one_time_donation/<charity_id>/<amount>', methods=('GET', 'POST'))
@login_required
def confirm_one_time_donation(charity_id, amount):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=current_user.id).first()
    confirm_form = ConfirmAmountForm()
    if confirm_form.validate_on_submit():
        donation = Donation(
            amount=amount,
            donor=donor,
            charity=charity
        )
        donation.process_donation()
        flash('Donation made succesfully!', 'good')
        return redirect(url_for('organization.one_time_donation_page', charity_id=donation.charity.id))
    return render_template('confirm_one_time_payment.html',
                           confirm_form=confirm_form,
                           amount=amount,
                           charity=charity)


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





