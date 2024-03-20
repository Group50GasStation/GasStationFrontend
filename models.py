from . import db

# This file contains all models used in our database. Effectively, this specifies to SQLAlchemy the
# tables to create/access when the app is running, with each class being a table - code in __init__.py
# will automatically create the database using this file as a reference if it doesn't exist locally.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(100))
