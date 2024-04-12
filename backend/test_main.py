import unittest
from backend import create_app
from backend.models import db
from backend.main import ProfileForm

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
        self.assertEqual(response.status_code, 302)  # Expect success

    def test_profileForm_validation(self):
        with self.app.application.app_context():
            form = ProfileForm()
            form.first_name.data = 'John'
            form.last_name.data = 'Wick'
            form.username.data = 'MrWick'
            form.email.data = "JW@continental.com"

            # Wrong email type
            form.email.data = "JW.com"
            self.assertEqual(form.validate(), False)  
            
            # PW not match
            form.password.data = 'HighTableSucks123'
            form.confirmed_password.data = 'HighTableSucks456'
            self.assertEqual(form.validate(), False)  

            form.address_primary.data = '123 Continental St'
            form.city.data = 'New York'
            form.state.data = 'NY'
            form.zipcode.data = 12345
            
    # Add more tests for other routes and functionalities as needed

if __name__ == '__main__':
    unittest.main()
