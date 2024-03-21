from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, ValidationError, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # No index page, so just redirect user to login
    return redirect(url_for('auth.login'))

# TODO: Add validators for all of these fields - check length, format, etc - try to use
# WTForms built in validators where possible
class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Confirmed password should match other password.")])
    address_primary = StringField('Address 1', validators=[DataRequired()])
    address_secondary = StringField('Address 2', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    # Good lord the below was not fun to type, even with macro assistance
    state = SelectField('State', choices=[("AL", "Alabama"),("AK", "Alaska"),("AZ", "Arizona"),("AR", "Arkansas"),("CA", "California"),
                                          ("CO", "Colorado"),("CT", "Connecticut"),("DE", "Delaware"),
                                          ("DC", "District of Columbia"),("FL", "Florida"),("GA", "Georgia"),
                                          ("HI", "Hawaii"),("ID", "Idaho"),("IL", "Illinois"),("IN", "Indiana"),
                                          ("IA", "Iowa"),("KS", "Kansas"),("KY", "Kentucky"),("LA", "Louisiana"),
                                          ("ME", "Maine"),("MD", "Maryland"),("MA", "Massachusetts"),("MI", "Michigan"),
                                          ("MN", "Minnesota"),("MS", "Mississippi"),("MO", "Missouri"),
                                          ("MT", "Montana"),("NE", "Nebraska"),("NV", "Nevada"),("NH", "New Hampshire"),
                                          ("NJ", "New Jersey"),("NM", "New Mexico"),("NY", "New York"),
                                          ("NC", "North Carolina"),("ND", "North Dakota"),("OH", "Ohio"),
                                          ("OK", "Oklahoma"),("OR", "Oregon"),("PA", "Pennsylvania"),
                                          ("RI", "Rhode Island"),("SC", "South Carolina"),("SD", "South Dakota"),
                                          ("TN", "Tennessee"),("TX", "Texas"),("UT", "Utah"),
                                          ("VT", "Vermont"),("VA", "Virginia"),("WA", "Washington"),
                                          ("WV", "West Virginia"),("WI", "Wisconsin"),("WY", "Wyoming")], validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    submit = SubmitField('Apply changes')

@main.route('/profile')
@login_required
def profile():
    form = ProfileForm(obj={'email':current_user.email, 'first_name':current_user.first_name,
                            'last_name':current_user.last_name, 'username':current_user.username,
                            'address_primary':current_user.address_primary,
                            'address_secondary':current_user.address_secondary,
                            'state':current_user.state,
                            'city':current_user.city, 'zipcode': current_user.zipcode})
    return render_template('profile.html', form=form)

@main.route('/profile', methods=['POST'])
def profile_post():
    form = ProfileForm()
    if form.validate_on_submit():
        #TODO: Persist changes to db
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form)

@main.route('/fuelquote')
@login_required
def new_fuel_quote_page():
    return render_template('fuelQuote.html')

@main.route('/quotehistory')
@login_required
def quote_history_page():
    # TODO: This will need... quite a few things passed to it to populate history from db
    return render_template('quoteHistory.html')
