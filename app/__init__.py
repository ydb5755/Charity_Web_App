from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import atexit
from threading import Thread
from datetime import datetime
from flask_apscheduler import APScheduler

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
scheduler = APScheduler()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    from app.models import Donor, Charity

    @login_manager.user_loader
    def load_user(user_id):
        donor = Donor.query.get(user_id)
        charity = Charity.query.get(user_id)
        if donor:
            return donor
        elif charity:
            return charity
        else:
            return None
    login_manager.login_view = 'main.login'
    from app.donor import donor
    from app.organization import organization
    from app.main import main
    app.register_blueprint(main)
    app.register_blueprint(donor)
    app.register_blueprint(organization)


    return app
