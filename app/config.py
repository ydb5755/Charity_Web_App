import os


class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # postgres://mypledge_user:juW0qNB4xRODGuv8vtxNhjPIKHBUB9dT@dpg-chlg51u7avj217cdrmlg-a.ohio-postgres.render.com/mypledge
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SCHEDULER_API_ENABLED = True