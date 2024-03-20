from flask import Blueprint
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # No index page, so just direct user to login
    return render_template('login.html')

@main.route('/profile')
def profile_page():
    return render_template('profile.html')

@main.route('/fuelquote')
def new_fuel_quote_page():
    return render_template('fuelQuote.html')

@main.route('/quotehistory')
def quote_history_page():
    return render_template('quoteHistory.html')
