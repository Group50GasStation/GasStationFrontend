from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import SelectField, StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp, Optional, NumberRange
from backend.models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # No index page, so just redirect user to login
    return redirect(url_for('auth.login'))


class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First name', validators=[DataRequired(), Length(min = 2, max=25)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min = 2, max=25)])
    username = StringField('Username', validators=[DataRequired(), Length(min = 4, max=20)])
    password = PasswordField('Password', validators=[Optional(), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,}$',
                                                                        message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character")])
    confirmed_password = PasswordField('Confirm Password', validators=[EqualTo('password', message="Confirmed password should match other password.")])
    address_primary = StringField('Address 1', validators=[DataRequired(), Length(min=2, max=100)])
    address_secondary = StringField('Address 2', validators=[Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
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
    zipcode = IntegerField('Zipcode', render_kw={"min": "10000", "max": "99999"}, validators=[DataRequired(), NumberRange(min=10000, max=99999)])
    submit = SubmitField('Apply changes')
    def to_string(self): # pragma: no cover
        result = ""
        for field in self:
            result += f"{field.label.text}: {field.data}\n"
        return result

@main.route('/profile')
@login_required
def profile(): # pragma: no cover
    form = ProfileForm()
    form.email.data = current_user.email
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.username.data = current_user.username
    form.address_primary.data = current_user.address_primary
    form.address_secondary.data = current_user.address_secondary
    form.state.data = current_user.state
    form.city.data = current_user.city
    form.zipcode.data = current_user.zipcode
    return render_template('profile.html', form=form)

@main.route('/profile', methods=['POST'])
def profile_post(): # pragma: no cover
    form = ProfileForm()
    if form.validate_on_submit():
        db_user = User.query.filter_by(email=current_user.email).first()
        if db_user: # This should never be None, as user must be logged in
            db_user.email = form.email.data
            db_user.first_name = form.first_name.data
            db_user.last_name = form.last_name.data
            db_user.username = form.username.data
            db_user.address_primary = form.address_primary.data
            db_user.address_secondary = form.address_secondary.data
            db_user.state = form.state.data
            db_user.city = form.city.data
            db_user.zipcode = form.zipcode.data

            if form.password.data:
                db_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16)

            db.session.commit()
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form)
