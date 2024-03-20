from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import models
from os.path import exists

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # TODO: Fix this to actually use a secret key properly, should
    # be pulled from a local gitignored file
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # everything not related to auth
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Setup database
    if not exists("db.sqlite"):
        db.create_all(app=app)
    db.init_app(app)

    return app
