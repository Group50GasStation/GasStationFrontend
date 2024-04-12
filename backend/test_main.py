import unittest
from backend import create_app
from backend.models import db, User
from backend.main import ProfileForm
from flask_login import login_user

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

            # Okay form
            form.first_name.data = "Valid"
            form.last_name.data = "Form"
            form.username.data = 'Validman'
            form.email.data = "validemail@gmail.com"
            form.address_primary.data = '123 Continental St'
            form.city.data = 'New York'
            form.state.data = 'NY'
            form.zipcode.data = 12345
            form.password.data = 'Admin1!'
            form.confirmed_password.data = 'Admin1!'
            self.assertEqual(form.validate(), True)

if __name__ == '__main__':
    unittest.main()
