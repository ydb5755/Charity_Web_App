from app.main import main
from flask import render_template, url_for
from app.models import Charity

@main.route('/')
def home():
    all_charities = Charity.query.all()
    return render_template('', 
                           all_charities=all_charities)