from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# This file contains all models used in our database. Effectively, this specifies to SQLAlchemy the
# tables to create/access when the app is running, with each class being a table - code in other files
# will automatically create the database using this file as a reference if it doesn't exist locally.

# Table of all users.
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address_primary = db.Column(db.String(100))
    address_secondary = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)
    quotes = relationship("Quote", back_populates="customer")

# Table of all fuel quotes. Multiple quotes from the same user will share the same user_id.
class Quote(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True) # Specific id of the quote
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    delivery_address = db.Column(db.String(100))
    date = db.Column(db.Date)
    gallons_requested = db.Column(db.Integer)
    suggested_price = db.Column(db.Float)
    amount_due = db.Column(db.Float)
    customer = relationship("User", back_populates="quotes")

# REMEMBER: When adding classes here or modifying them, you should delete the db.sqlite file
# to allow SQLAlchemy to create it anew with the new tables. Failing to do so can cause issues.
