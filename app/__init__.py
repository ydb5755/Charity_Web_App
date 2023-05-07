from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    from app.models import Donor, Charity, Admin

    @login_manager.user_loader
    def load_user(user_id):
        if session['account_type'] == 'Donor':
            return Donor.query.get(int(user_id))
        elif session['account_type'] == 'Charity':
            return Charity.query.get(int(user_id))
        elif session['account_type'] == 'Admin':
            return Admin.query.get(int(user_id))
        else:
            return None

    from app.donor import donor
    from app.organization import organization
    from app.main import main
    app.register_blueprint(main)
    app.register_blueprint(donor)
    app.register_blueprint(organization)

    return app
