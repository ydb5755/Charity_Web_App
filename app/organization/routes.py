from app.organization import organization
from flask import render_template


@organization.route('/charity_page/<org_id>')
def charity_page(org_id):
    return render_template('')