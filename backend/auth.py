from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, ValidationError, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp
from backend.models import *

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=30),
                                                     Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,}$',
                                                            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character")])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')
    def to_string(self):
        result = ""
        for field in self:
            result += f"{field.label.text}: {field.data}\n"
        return result

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
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=30),
                                                     Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,}$',
                                                            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character")])
    confirmed_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=5, max=30),
                                                                       EqualTo('password', message="Confirmed password must match original password")])
    submit = SubmitField('Submit')
    def to_string(self):
        result = ""
        for field in self:
            result += f"{field.label.text}: {field.data}\n"
        return result

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

        if not register_new_user(email, name, password):
            form.email.errors = ['Account with this email already exists, please login instead.']
        else: # Registration successful
            return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)


# Takes information for a User, ensures they don't already exist, then adds to the userbase.
# Returns True/false depending on success.
def register_new_user(email, name, password):
    new_user = User(email=email, username=name, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=16))
    if User.query.filter_by(email=email).first(): # If user already present in db
        return False
    else:
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return True

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
