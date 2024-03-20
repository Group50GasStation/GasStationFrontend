import os
from flask import Flask
from .models import *

def create_app():
    app = Flask(__name__)

    # TODO: Fix this to actually use a secret key properly, should
    # be pulled from a local gitignored file
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    # Get the path of the app directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # everything not related to auth
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    # Create the database tables, and file if it doesn't exist
    with app.app_context():
        db.create_all()

    return app
