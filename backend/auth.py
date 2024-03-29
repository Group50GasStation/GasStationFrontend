from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, ValidationError, PasswordField
from wtforms.validators import DataRequired, EqualTo
from backend.models import *

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')
    def validate_email(self, field):
        email = field.data
        if not is_valid_email(email):
            raise ValidationError("Email is not in a valid format.")
    def validate_password(self, field):
        if len(field.data) > 30 or len(field.data) < 5:
            raise ValidationError("Password is of invalid length")

# This also serves as a route to login, along with the root /
@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        remember = form.remember.data
        db_user = User.query.filter_by(email=email).first()

        if db_user and check_password_hash(db_user.password, form.password.data):
            # Login success, so log them in and send them to their profile
            login_user(db_user, remember=remember)
            return redirect(url_for('main.profile'))
        else:
            form.password.errors = ['Wrong password or email.']
    return render_template('login.html', form=form)


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Confirmed password must match original password")])
    submit = SubmitField('Submit')
    def validate_email(self, field):
        email = field.data
        if not is_valid_email(email):
            raise ValidationError("Email is not in a valid format.")

@auth.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@auth.route('/register', methods=['POST'])
def register_post():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.username.data
        password = form.password.data

        if User.query.filter_by(email=email).first(): # If user already present in db
            #raise ValidationError("Account with this email already exists, please login instead.")
            form.email.errors = ['Account with this email already exists, please login instead.']
            print("bad")
        else:
            # add the new user to the database
            new_user = User(email=email, username=name, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=16))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    print(form.email.errors)
    return render_template("register.html", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Helper function to check if an email is in the correct format.
# TODO: This should be unit tested later
def is_valid_email(email):
    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex, email)
