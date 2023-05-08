from app.organization import organization
from flask import render_template, redirect, url_for
from flask_login import login_required


@organization.route('/charity_page/<org_id>')
@login_required
def charity_personal_page(org_id):
    
    return render_template('')