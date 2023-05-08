from app.organization import organization
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Charity
from app import db


@organization.route('/charity_personal_page/<org_id>')
@login_required
def charity_personal_page(org_id):
    
    return render_template('')

@organization.route('/charity_page/<org_id>')
@login_required
def charity_page(org_id):
    
    return render_template('charity_page.html')

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