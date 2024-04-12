import unittest
from backend import create_app
from backend.models import db
from backend.fuelquote import *

class TestFuelquoteBlueprint(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.application.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_fuel_price(self):
        # TODO: This should call the get_fuel_price() function from fuelquote.py
        # and test it with several values, ensuring it arrives at the right price.
        self.assertEqual(True, True)

    def test_persist_quote(self):
        # TODO: This should create a quote, persist it, then attempt
        # to pull it back up from the db. Make several assert calls along the way.
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
