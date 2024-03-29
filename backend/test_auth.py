import unittest
from flask import url_for
from backend import create_app
from backend.models import db
from backend.auth import LoginForm, RegisterForm, register_new_user


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
            form.password.data = "Password5!"
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
            form.password.data = "Wow!32323dudethispasswordiswayyytoooooolongggggImeanwayyyytooooodamnlonggggggggggg"
            self.assertEqual(form.validate(), False)
            # Pwd too short
            form.password.data = "No1!"
            self.assertEqual(form.validate(), False)
            # Pwd too simple
            form.password.data = "password"
            self.assertEqual(form.validate(), False)

    def test_login_form_okay(self):
        with self.app.application.app_context():
            form = LoginForm()
            form.email.data = "blah@something.com"
            form.password.data = "Password!234"
            self.assertEqual(form.validate(), True)


    # REGISTER TESTS ------------------

    def test_register_page_loads(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)  # Expect success

    def test_register_form_bad_email(self):
        with self.app.application.app_context():
            form = RegisterForm()
            form.email.data = "blah@something"
            form.password.data = "Password5!"
            form.confirmed_password.data = "Password5!"
            form.username.data = "testusername"
            self.assertEqual(form.validate(), False)
            form.email.data = "blah.com"
            self.assertEqual(form.validate(), False)
            form.email.data = "test@.com"
            self.assertEqual(form.validate(), False)

    def test_register_form_bad_password(self):
        with self.app.application.app_context():
            form = RegisterForm()
            form.password.data = "Password5!"
            form.confirmed_password.data = "Password5!"
            form.username.data = "testusername"
            form.email.data = "blah@something.com"
            # Pwd too long
            form.password.data = "Wow!43382dudethispasswordiswayyytoooooolongggggImeanwayyyytooooodamnlonggggggggggg"
            form.confirmed_password.data = "Wow!43382dudethispasswordiswayyytoooooolongggggImeanwayyyytooooodamnlonggggggggggg"
            self.assertEqual(form.validate(), False)
            # Pwd too short
            form.password.data = "No!2"
            form.confirmed_password.data = "No!2"
            self.assertEqual(form.validate(), False)
            # Pwds don't match
            form.password.data = "Something!1234"
            form.confirmed_password.data = "Something_else!5678"
            self.assertEqual(form.validate(), False)
            # Pwd too simple
            form.password.data = "password"
            form.confirmed_password.data = "password"
            self.assertEqual(form.validate(), False)

    def test_register_form_okay(self):
        with self.app.application.app_context():
            form = RegisterForm()
            form.password.data = "Hunter2!"
            form.confirmed_password.data = "Hunter2!"
            form.username.data = "testusername"
            form.email.data = "blah@something.com"
            self.assertEqual(form.validate(), True)

    def test_register_a_new_user(self):
        with self.app.application.app_context():
            password = "Hunter2!"
            username = "newguy"
            email = "newguy@site.com"
            self.assertEqual(register_new_user(email, username, password), True)


if __name__ == '__main__':
    unittest.main()
