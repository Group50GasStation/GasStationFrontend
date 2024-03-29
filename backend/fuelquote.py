from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, EqualTo
from backend.models import *

fuelquote = Blueprint('fuelquote', __name__)

class NewQuoteForm(FlaskForm):
    gallons_requested = IntegerField('Gallons requested', validators=[DataRequired()])
    delivery_address = StringField('Delivery address',
                                   render_kw={'readonly': True, 'title':"Go to profile to modify delivery address."},
                                   validators=[DataRequired()])
    delivery_date = DateField('Delivery date', validators=[DataRequired()])
    suggested_price = FloatField('Suggested price/gallon', render_kw={'readonly': True}, validators=[DataRequired()])
    amount_due = FloatField('Total amount due', render_kw={'readonly': True}, validators=[DataRequired()])
    submit_dryrun = SubmitField('Get quote')
    submit = SubmitField('Submit request')

@fuelquote.route('/new_quote')
@login_required
def new_fuel_quote():
    form = NewQuoteForm()
    form.delivery_address.data = current_user.address_primary + "," + current_user.address_secondary

    return render_template('new_fuel_quote.html', form=form)

@fuelquote.route('/new_quote', methods=["POST"])
@login_required
def new_fuel_quote_post():
    form = NewQuoteForm()
    # TODO: (assign 5) Validate all fields, make call to pricing module,
    # and make entry to DB if non-dryrun button clicked
    return render_template('new_fuel_quote.html', form=form)

@fuelquote.route('/quote_history')
@login_required
def quote_history():
    # TODO: (assign 5) This will need to populate history from db
    return render_template('quote_history.html')
