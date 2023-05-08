from app.donor import donor
from flask import render_template, redirect, flash, url_for
from app.models import Donor, Charity
from flask_login import current_user, login_required
from app.donor.forms import AddAdmin, RemoveAdmin
from app import db


@donor.route('/profile/<donor_id>')
@login_required
def profile_page(donor_id):
    if not current_user.id == donor_id:
        return redirect(url_for('main.home'))
    donor = Donor.query.filter_by(id=donor_id).first()
    if donor.admin:
        charities_to_be_confirmed = Charity.query.filter_by(authenticated=False)
        add_admin_form = AddAdmin()
        if add_admin_form.validate_on_submit():
            user = Donor.query.filter_by(id=add_admin_form.id.data).first()
            user.admin = True
            db.session.commit()
            flash('Admin priviliges added to user')
            return redirect(url_for('donor.profile_page', donor_id=current_user.id))
        remove_admin_form = RemoveAdmin()
        remove_admin_form.choices = [(user.email) for user in Donor.query.filter_by(admin=True)].remove(Donor.query.filter_by(id=1).first())
        if remove_admin_form.validate_on_submit():
            user = Donor.query.filter_by(email=remove_admin_form.admin.data)
            user.admin = False
            db.session.commit()
            flash('Admin priviliges removed from user')
            return redirect(url_for('donor.profile_page', donor_id=current_user.id))
    return render_template('profile.html',
                           donor=donor,
                           charities_to_be_confirmed=charities_to_be_confirmed,
                           add_admin_form=add_admin_form,
                           remove_admin_form=remove_admin_form)

