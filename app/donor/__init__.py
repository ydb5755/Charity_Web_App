from flask import Blueprint

donor = Blueprint('donor', __name__,static_folder='static', template_folder='templates', url_prefix='/donor')

from app.donor import routes