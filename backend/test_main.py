import unittest
from flask import url_for
from GasStationFrontend import create_app, db
 # Change with actual flask app name
from .models import User # Change with actual flask app name

class TestAuthBlueprint(unittest.TestCase):

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

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)  # Expect success

    # Add more tests for login, registration, and logout functionalities as needed

class TestMainBlueprint(unittest.TestCase):

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

    def test_index_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Expect redirect

    def test_profile_page_loads(self):
        # Assuming authentication, so we need to simulate a logged-in user
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1  # Assuming user ID 1 exists in our database
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)  # Expect success

    # Add more tests for other routes and functionalities as needed

if __name__ == '__main__':
    unittest.main()
