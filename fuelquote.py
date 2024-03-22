from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, ValidationError, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from .models import *

fuelquote = Blueprint('fuelquote', __name__)

class NewQuoteForm(FlaskForm):
    #email = StringField('Email', validators=[DataRequired()])
    #password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@fuelquote.route('/new_quote')
@login_required
def new_fuel_quote():
    return render_template('new_fuel_quote.html')

@fuelquote.route('/new_quote', methods=["POST"])
@login_required
def new_fuel_quote_post():
    return render_template('new_fuel_quote.html')

@fuelquote.route('/quote_history')
@login_required
def quote_history():
    # TODO: This will need... quite a few things passed to it to populate history from db
    return render_template('quote_history.html')
