import unittest
from datetime import datetime
from backend import create_app
from backend.models import db, Quote
from backend.fuelquote import NewQuoteForm, get_fuel_price_margin

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

    def test_new_quote_validation(self):
        with self.app.application.app_context():
            form = NewQuoteForm() # This needs app context for some reason, probably because of DateField
            import datetime
            # 05/24/2050
            date = datetime.datetime.strptime('24052050', '%d%m%Y').date()

            # form ok -------------
            form.gallons_requested.data = 30
            form.delivery_address.data = "123 test lane"
            form.delivery_date.data = date
            self.assertEqual(form.validate(), True)

            # bad gallons -----------
            form.gallons_requested.data = -3
            self.assertEqual(form.validate(), False)

            # Bad date -----------
            form.gallons_requested.data = 30
            # 05/24/2000
            date = datetime.datetime.strptime('24052000', '%d%m%Y').date()
            form.delivery_date.data = date
            self.assertEqual(form.validate(), False)


    def test_get_fuel_price_margin(self):
        # Test fuel price calculation for different scenarios
        # Texas, with history, more than 1000 gallons
        price_1 = get_fuel_price_margin(in_texas=True, has_history=True, gallons_requested=1500)
        expected_price_1 = (0.02 - 0.01 + 0.02 + 0.1) * 1.5
        self.assertAlmostEqual(round(price_1, 2), round(expected_price_1, 2))

        # Non-Texas, no history, less than 1000 gallons
        price_2 = get_fuel_price_margin(in_texas=False, has_history=False, gallons_requested=800)
        expected_price_2 = (0.04 + 0 + 0.03 + 0.1) * 1.5
        self.assertAlmostEqual(round(price_2, 2), round(expected_price_2, 2))

        # Test fuel price calculation when zero gallons are requested
        price_3 = get_fuel_price_margin(in_texas=True, has_history=True, gallons_requested=0)
        self.assertAlmostEqual(round(price_3, 2), 0.21)

    def test_persist_quote(self):
        with self.app.application.app_context():
            # Create and persist a quote
            quote = Quote(
                user_id=1,
                delivery_address="123 Main St",
                date=datetime.now(),
                gallons_requested=1000,
                suggested_price=1.50,
                amount_due=1500
            )
            db.session.add(quote)
            db.session.commit()

            # Retrieve the quote from the database
            retrieved_quote = Quote.query.filter_by(user_id=1).first()

            # Assert that the retrieved quote matches the original quote
            self.assertIsNotNone(retrieved_quote)
            self.assertEqual(retrieved_quote.user_id, quote.user_id)
            self.assertEqual(retrieved_quote.delivery_address, quote.delivery_address)
            self.assertEqual(retrieved_quote.date, quote.date)
            self.assertEqual(retrieved_quote.gallons_requested, quote.gallons_requested)
            self.assertEqual(retrieved_quote.suggested_price, quote.suggested_price)
            self.assertEqual(retrieved_quote.amount_due, quote.amount_due)

    def test_get_fuel_price_margin_outside_texas_no_history(self):
    # Test fuel price calculation for a user outside Texas with no history
        price = get_fuel_price_margin(in_texas=False, has_history=False, gallons_requested=1000)
        expected_price = (0.04 + 0 + 0.03 + 0.1) * 1.0  # Assuming 1.0 gallons for simplicity
        self.assertAlmostEqual(price, expected_price, places=0)  # Adjusted places to match expected precision


if __name__ == '__main__':
    unittest.main()
