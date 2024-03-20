from flask import Blueprint
from . import db

auth = Blueprint('auth', __name__)

# This also serves as a route to login, along with the root /
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/register')
def signup():
    return render_template('register.html')

# TODO: Change this later to a proper logout system + redirect
@auth.route('/logout')
def logout():
    return 'Logout'
