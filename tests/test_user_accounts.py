import unittest
import json
from app import *

class AuthTestCase(unittest.TestCase):
    """
    This class represents user registration and login test cases
    """

    def setUp(self):
        """
        Initialise app, test client and test variables
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_details = {
        'username':'admin',
        'email':'admin@gmail.com',
        'password':'adminpass'
        }
        with self.app.app_context():
            db.create_all()
    
    def test_successful_registration(self):
        """
        Test whether API can register a user 
        """
        
        res = self.client().post('/auth/register', data=self.user_details)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Registration successful.")

    def test_already_registered_user(self):
        """
        Test that a user cannot register twice
        """
        res = self.client().post('/auth/register', data=self.user_details)
        secondres = self.client().post('/auth/register', data=self.user_details)
        result = json.loads(secondres.data.decode())
        self.assertEqual(result['message'], "You are already registered. Please login.")

    def test_password_length(self):
        """
        Test that a password must be 6 characters long
        """
        details = {
        'username': 'newuser',
        'email': 'newuser@gmail.com',
        'password': 'new'
        }
        res = self.client().post('/auth/register', data=details)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Password is either too short or empty."\
            "Please try again.")

    def test_invalid_email(self):
        """
        Test that an email must be valid
        """
        details = {
        'username': 'newuser',
        'email': 'newuser.com',
        'password': 'newpass'
        }
        res = self.client().post('/auth/register', data=details)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Email Invalid."\
            "Do not include special characters or leave the field empty.")

    def test_invalid_username(self):
        """
        Test that a username must be valid
        """
        details = {
        'username': '+-==-=',
        'email': 'newuser.com',
        'password': 'newpass'
        }
        res = self.client().post('/auth/register', data=details)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Username can neither include special"\
            "characters nor be empty.")

    def test_login(self):
        """
        Test that a user with an account can login
        """
        res = self.client().post('/auth/register', data=self.user_details)
        login_res = self.client().post('/auth/login', data=self.user_details)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_login_without_account(self):
        """
        Test that a user needs to be registered to login
        """
        unregistered_user = {
        'username': 'nonuser',
        'email': 'notuser@gmail.com',
        'password': 'nonpass'
        }
        res = self.client().post('/auth/login', data=unregistered_user)
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Login unsuccessful."\
            "Please register or confirm details.")

    def test_empty_password(self):
        """
        Test a user cannot leave password field empty
        """
        res = self.client().post('/auth/register', data=self.user_details)
        login_res = self.client().post('/auth/login', data={
            'username': 'admin',
            'email': 'admin@gmail.com',
            'password': ''})
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "Password cannot be empty.")

    def test_empty_email(self):
        """
        Test a user cannot leave email field empty
        """
        res = self.client().post('/auth/register', data=self.user_details)
        login_res = self.client().post('/auth/login', data={
            'username': 'admin',
            'email': '',
            'password': 'adminpass'})
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "Email cannot be empty.")

    def test_empty_username(self):
        """
        Test a user cannot leave username field empty
        """
        res = self.client().post('/auth/register', data=self.user_details)
        login_res = self.client().post('/auth/login', data={
            'username': '',
            'email': 'admin@gmail.com',
            'password': 'adminpass'})
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "Username cannot be empty.")
       
    def tearDown(self):
        """
        Delete all initialized variables
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()



