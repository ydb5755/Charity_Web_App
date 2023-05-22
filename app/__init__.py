from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from flask_apscheduler import APScheduler
from werkzeug.security import generate_password_hash

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
    login_manager.login_view = 'main.login_donor'
    from app.donor import donor
    from app.organization import organization
    from app.main import main
    app.register_blueprint(main)
    app.register_blueprint(donor)
    app.register_blueprint(organization)


    return app


from app.models import Donor, Charity
def populate():
    admin = Donor(
                first_name      = 'Yisroel',
                last_name       = 'Baum',
                address         = 'Someplace or other',
                zip_code        = '9945623',
                phone_cell      = '0258795461',
                email           = 'yisroel.d.baum@gmail.com',
                password        = generate_password_hash('12', method='scrypt'),
                bank            = '0',
                account_number  = '0',
                name_on_account = 'yisroel baum',
                admin = True
    )
    for x in range(50):
        donor = Donor(
                    first_name      = f'user{x}fn',
                    last_name       = f'user{x}ln',
                    address         = f'{x} Jerusalem Road',
                    zip_code        = f'{x + 10000}',
                    phone_home      = '0' + f'{x + 721234500}',
                    phone_cell      = '0' + f'{x + 587061230}',
                    email           = f'user{x}@gmail.com',
                    password        = generate_password_hash('12', method='scrypt'),
                    bank            = '0',
                    account_number  = f'{x + 1}',
                    name_on_account = f'user{x}fn user{x}ln'
        )
        charity = Charity(
                        id               = x + 5010,
                        charity_name     = f'charity{x}',
                        address          = f'{x} Tel Aviv Road',
                        zip_code         = f'{x + 20000}',
                        phone            = '0' + f'{x + 723201250}',
                        website          = f'charity{x}.com',
                        email            = f'charity{x}@gmail.com',
                        password         = generate_password_hash('12', method='scrypt'),
                        contact_name     = f'contact number {x}',
                        contact_cell     = '0' + f'{x + 546217512}',
                        contact_position = 'Charity Collector',
                        bank             = '0',
                        account_number   = f'{x + 12305}'
        )
        if charity.id < 5040:
            charity.authenticated = True
        db.session.add(donor)
        db.session.add(charity)
    db.session.add(admin)
    db.session.commit()

