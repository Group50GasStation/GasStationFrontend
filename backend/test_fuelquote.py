import unittest
from flask import url_for
from backend import create_app
from backend.models import db
from backend.fuelquote import NewQuoteForm

class TestfuelQuoteBlueprint(unittest.TestCase):
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
    
    # Tests below here -------------------
    
    def test_bad_galon(self):
        with self.app.application.app_context():
            quote = NewQuoteForm()
            # Galon includes string
            quote.gallons_requested.data = "Price123"
            self.assertEqual(quote.validate(), False)

    def test_bad_date(self):
        with self.app.application.app_context():
            quote = NewQuoteForm()
            # Date include string
            quote.delivery_date.data = "23th April 2024"
            self.assertEqual(quote.validate(), False)

    def test_bad_price(self):
        with self.app.application.app_context():
            quote = NewQuoteForm()
            # Price is integer
            quote.suggested_price.data = 22
            self.assertEqual(quote.validate(), False)

            # Amount due is integer
            quote.amount_due.data = 22
            self.assertEqual(quote.validate(), False)


if __name__ == '__main__':
    unittest.main()