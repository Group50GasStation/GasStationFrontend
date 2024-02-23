from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/fuelquote')
def new_fuel_quote_page():
    return render_template('fuelQuote.html')
