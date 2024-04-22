from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from datetime import date
from wtforms import DateField, StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, NumberRange
from backend.models import *

fuelquote = Blueprint('fuelquote', __name__)

class NewQuoteForm(FlaskForm):
    gallons_requested = IntegerField('Gallons requested', validators=[DataRequired(), NumberRange(min=1, max=9223372036854775807)]) #prevent overflow error when converting to sqllite signed int
    delivery_address = StringField('Delivery address',
                                   render_kw={'readonly': True, 'title': "Go to profile to modify delivery address."},
                                   validators=[DataRequired()])

    # Ensures the provided date is in the future.
    def future_date(self, field):
        if field.data <= date.today():
            raise ValidationError('Delivery date must be in the future.')

    delivery_date = DateField('Delivery date', validators=[DataRequired(), future_date])
    submit_dryrun = SubmitField('Get quote')
    submit = SubmitField('Submit request')

    def to_string(self): # pragma: no cover
        result = ""
        for field in self:
            result += f"{field.label.text}: {field.data}\n"
        return result

@fuelquote.route('/new_quote')
@login_required
def new_fuel_quote():
    form = NewQuoteForm()
    if current_user.address_primary and current_user.address_secondary:
        form.delivery_address.data = current_user.address_primary + ", " + current_user.address_secondary + ", " + current_user.city + ", " + current_user.state + ", " + str(current_user.zipcode)
    elif current_user.address_primary: # No secondary address
        form.delivery_address.data = current_user.address_primary + ", " + current_user.city + ", " + current_user.state + ", " + str(current_user.zipcode)

    return render_template('new_fuel_quote.html', form=form, price_per_gallon = 0, amount_due = 0)

@fuelquote.route('/new_quote', methods=["POST"])
@login_required
def new_fuel_quote_post():
    form = NewQuoteForm()
    price_per_gallon = 0
    amount_due = 0
    if form.validate_on_submit():
        # If any quote entries exist for the current user's id
        has_history = (Quote.query.filter_by(user_id=current_user.id).count() > 0)
        # If user's state is texas
        in_texas = (current_user.state == "TX")

        #cannot round this down to the next cent if we want to maintain price accuracy
        price_per_gallon = 1.50 + get_fuel_price_margin(in_texas, has_history, form.gallons_requested.data)
        amount_due = round(price_per_gallon * form.gallons_requested.data, 2)

        # Then, if they clicked the submit request button
        if form.submit.data:
            #persist to db then send to history page
            new_quote = Quote(user_id = current_user.id, delivery_address = form.delivery_address.data, date = form.delivery_date.data,
                              gallons_requested = form.gallons_requested.data, suggested_price = price_per_gallon,
                              amount_due=amount_due)
            db.session.add(new_quote)
            db.session.commit()
            return redirect(url_for('fuelquote.quote_history'))

    # else, they just clicked the dryrun button, so refresh updated form with new values.
    return render_template('new_fuel_quote.html', form=form, price_per_gallon=price_per_gallon, amount_due=amount_due)

# The "pricing module" - determines price per gallon based on args.
# Takes 2 bools and the number of gallons requested.
# Returns price per gallon, should then be multiplied by gallons requested.
def get_fuel_price_margin(in_texas, has_history, gallons_requested):
    location_factor = 0.02          # 2% for texas, 4% for out of state.
    rate_history_factor = 0.0       # 1% if prior history, otherwise 0%
    gallons_requested_factor = 0.03 # 2% if more than 1k gallons, 3% if less
    company_profit_factor = 0.1     # always 10%

    if not in_texas:
        location_factor = 0.04
    if has_history:
        rate_history_factor = 0.01
    if gallons_requested > 1000:
        gallons_requested_factor = 0.02

    return (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor) * 1.5

@fuelquote.route('/quote_history')
@login_required
def quote_history():
    quotes = Quote.query.filter_by(user_id=current_user.id)
    return render_template('quote_history.html', quotes = quotes)
