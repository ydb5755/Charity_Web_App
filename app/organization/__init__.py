from flask import Blueprint

organization = Blueprint('organization', __name__, static_folder='static', template_folder='templates', url_prefix='/organization')

from app.organization import routes