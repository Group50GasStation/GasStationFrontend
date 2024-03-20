from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired
from .models import *

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

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
        password = form.password.data
        remember = form.remember.data

        db_user = User.query.filter_by(email=email).first()

        if not db_user or not check_password_hash(db_user.password, password):
            raise ValidationError("Wrong email or password.")

        # Login success, so log them in and send them to their profile
        login_user(db_user, remember=remember)
        return redirect(url_for('main.profile'))
    return render_template('login.html', form=form)

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    # TODO: Add more robust validation here to make sure these values make sense, and if not, show error
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password_input')
    conf_password = request.form.get('confirm_pw')

    if User.query.filter_by(email=email).first(): # If user already present in db
        flash("User account already exists, please login instead.")
        return redirect(url_for('auth.register'))

    if password and conf_password and (password != conf_password):
        flash("Confirmed password did not match originally provided password.")
        return redirect(url_for('auth.register'))

    # add the new user to the database
    new_user = User(email=email, username=name, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=16))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
