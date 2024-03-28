import os
from flask import Flask
from flask_login import LoginManager
from GasStationFrontend.backend.models import *






def create_app():
    app = Flask(__name__)

    # TODO: Fix this to actually use a secret key properly, should
    # be pulled from a local gitignored file
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    # Get the path of the app directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Auth stuff like login and registering
    from GasStationFrontend.backend.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # everything not related to auth or fuel quotes
    from GasStationFrontend.backend.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Related to fuel quotes
    from GasStationFrontend.backend.fuelquote import fuelquote as fuelquote_blueprint
    app.register_blueprint(fuelquote_blueprint)

    db.init_app(app)

    # Create the database tables, and file if it doesn't exist
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
