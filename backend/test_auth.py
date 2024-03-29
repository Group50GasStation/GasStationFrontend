import unittest
from flask import url_for
from backend import create_app
from backend.models import db
from backend.auth import LoginForm


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

    # Tests below here -------------------


    # LOGIN TESTS ------------------
    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)  # Expect success

    def test_login_form_bad_email(self):
        with self.app.application.app_context():
            form = LoginForm()
            form.email.data = "blah@something"
            form.password.data = "password"
            self.assertEqual(form.validate(), False)
            form.email.data = "blah.com"
            self.assertEqual(form.validate(), False)
            form.email.data = "test@.com"
            self.assertEqual(form.validate(), False)

    def test_login_form_bad_password(self):
        with self.app.application.app_context():
            form = LoginForm()
            form.email.data = "blah@something.com"
            # Pwd too long
            form.password.data = "wowdudethispasswordiswayyytoooooolongggggImeanwayyyytooooodamnlonggggggggggg"
            self.assertEqual(form.validate(), False)
            # Pwd too short
            form.password.data = "no"
            self.assertEqual(form.validate(), False)

    def test_login_form_okay(self):
        with self.app.application.app_context():
            form = LoginForm()
            form.email.data = "blah@something.com"
            form.password.data = "password"
            self.assertEqual(form.validate(), True)


    # REGISTER TESTS ------------------

if __name__ == '__main__':
    unittest.main()
