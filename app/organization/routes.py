from app.organization import organization
from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Charity, Donor, Pledge, Donation
from app import db, scheduler
from app.organization.forms import RecurringDonationForm, SingleDonationForm
from datetime import datetime




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
    return redirect(url_for('organization.donation_page', charity_id=charity.id, donor_id=donor.id))


@organization.route('/one_time_donation/charity/<charity_id>/donor/<donor_id>', methods=('GET', 'POST'))
@login_required
def one_time_donation_page(charity_id, donor_id):
    charity = Charity.query.filter_by(id=charity_id).first()
    donor = Donor.query.filter_by(id=donor_id).first()
    sd_form = SingleDonationForm()
    if sd_form.validate_on_submit():
        donation = Donation(
            amount=float(sd_form.amount.data),
            donor=donor,
            charity=charity
        )
        donation.process_donation()
        return redirect(url_for('organization.donation_page', charity_id=charity.id, donor_id=donor.id))
    return render_template('one_time_donation_page.html',
                           charity=charity,
                           donor=donor,
                           sd_form=sd_form)





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