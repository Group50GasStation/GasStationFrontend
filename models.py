from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# This file contains all models used in our database. Effectively, this specifies to SQLAlchemy the
# tables to create/access when the app is running, with each class being a table - code in other files
# will automatically create the database using this file as a reference if it doesn't exist locally.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


# REMEMBER: When adding classes here or modifying them, you should delete the db.sqlite file
# to allow SQLAlchemy to create it anew with the new tables.
