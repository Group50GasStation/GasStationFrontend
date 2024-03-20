from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# This file contains all models used in our database. Effectively, this specifies to SQLAlchemy the
# tables to create/access when the app is running, with each class being a table - code in other files
# will automatically create the database using this file as a reference if it doesn't exist locally.

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    address_primary = db.Column(db.String(100))
    address_secondary = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)


# REMEMBER: When adding classes here or modifying them, you should delete the db.sqlite file
# to allow SQLAlchemy to create it anew with the new tables. Failing to do so can cause issues.
