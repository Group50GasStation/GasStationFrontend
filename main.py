from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # No index page, so just redirect user to login
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    # TODO: This will need to have any fields we populate from DB added to it, along with username
    return render_template('profile.html', username=current_user.username)

@main.route('/fuelquote')
@login_required
def new_fuel_quote_page():
    return render_template('fuelQuote.html')

@main.route('/quotehistory')
@login_required
def quote_history_page():
    # TODO: This will need... quite a few things passed to it to populate history from db
    return render_template('quoteHistory.html')
