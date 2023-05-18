from app.organization import organization
from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Charity, Donor, Pledge, Donation
from app import db, scheduler
from app.organization.forms import RecurringDonationForm, SingleDonationForm
from app.main.forms import CharitySignUpForm
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash





@organization.route('/authentication_details/<charity_id>', methods=('GET', 'POST'))
@login_required
def authentication_details(charity_id):
    if current_user.admin == False:
        return redirect(url_for('main.home'))
    update_form = CharitySignUpForm()
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
            
        if update_form.password.data != update_form.confirm_password.data:
            flash('Passwords do not match, please try again', 'bad')
            return redirect(url_for('organization.authentication_details',
                                    charity_id=charity.id))
        
        pw = generate_password_hash(update_form.password.data, method='scrypt')

        charity.id = update_form.id.data
        charity.charity_name = update_form.charity_name.data
        charity.address = update_form.address.data
        charity.zip_code = update_form.zip_code.data
        charity.phone = update_form.phone.data
        charity.website = update_form.website.data
        charity.email = update_form.email.data
        charity.password = pw
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


def pledge_transaction(pledge_id):
    with scheduler.app.app_context():
        pledge = Pledge.query.filter_by(id=pledge_id).first()
        if datetime.now() > pledge.end_date:
            return scheduler.remove_job(str(pledge.id))
        if datetime.now() > pledge.start_date:
            pledge.donor.balance -= pledge.amount
            pledge.charity.balance += pledge.amount
            db.session.commit()


def pledge_start_date(pledge_id):
    with scheduler.app.app_context():
        pledge = Pledge.query.filter_by(id=pledge_id).first()
        frequency = pledge.frequency
        if frequency == 'Month':
            scheduler.add_job(id=str(pledge_id), func=pledge_transaction, args=(pledge.id, ), trigger='cron', day=25, hour=12)
        else:
            scheduler.add_job(id=str(pledge_id), func=pledge_transaction, args=(pledge.id, ), trigger='interval', seconds=times.get(frequency))

times = {
    'Second':1,
    'Minute':60,
    'Hour':3600,
    'Day':86400,
    'Week':604800
}

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







        # t = Timer(10, pledge.process_pledge)
        # t.start()
        # scheduler.add_job(func=pledge.process_pledge(), trigger="date", run_date=dt_start)
        # x = Thread(target=pledge.process_pledge, daemon=True)
        # x.start()
        # pledge.process_pledge()


        #You only need one thread to keep on repeating one function which goes through all pledges every second and checks if "end > datetime.now() > start". If True, then process transaction \
        # using local_var saved time with frequency difference (start + frequency) 
        # (end-start)/frequency   -----   (10-2)/2 == 4 ---- 4-2 == 2
        # if now - start is divisible by frequency then process 

        
    # start = pledge.start_date.timestamp().__floor__()
    # end = pledge.end_date.timestamp().__floor__()
    # now = datetime.now().timestamp().__floor__()
    # while now <= end:
    #     if start <= now :
    #         if frequency == 'Month':
    #             pledge.donor.balance -= pledge.amount
    #             pledge.charity.balance += pledge.amount
    #             db.session.commit()
    #             pledge.start_date.year
    #             time.sleep(1)
    #             now = datetime.now().timestamp().__floor__()
    #             continue
    #         else:
    #             print(times.get(frequency))
    #             pledge.donor.balance -= pledge.amount
    #             pledge.charity.balance += pledge.amount
    #             db.session.commit()
    #             time.sleep(times.get(frequency))
    #             now = datetime.now().timestamp().__floor__()
    #             continue
    #     time.sleep(1)
    #     now = datetime.now().timestamp().__floor__()