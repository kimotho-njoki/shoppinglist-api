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
			db.drop_all()
			db.create_all()

	def test_registration(self):
		"""
		Test whether API can register a user
		"""
		res = self.client().post('/auth/register/', data=self.user_details)
		result = json.loads(res.data.decode())
		self.assertEqual(result['message'], "Registration successful.")
		self.assertEqual(result.status_code, 201)

	def test_already_registered_user(self):
		"""
		Test that a user cannot register twice
		"""
		res = self.client().post('/auth/register', data=self.user_details)
		self.assertEqual(res.status_code, 201)
		secondres = self.client().post('/auth/register', data=self.user_details)
		self.assertEqual(secondres.status_code, 202)
		result = json.loads(secondres.data.decode())
		self.assertEqual(result['message'], "You are already registered. Please login.")

	def test_login(self):
		"""
		Test that a user with an account can login
		"""
		res = self.client().post('/auth/register', data=self.user_details)
		self.assertEqual(res.status_code, 201)
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
		'username': 'nonuser'
		'email': 'non@gmail.com'
		'password': 'nonpass'
		}
		res = self.client().post('/auth/login', data=unregistered_user)
		result = json.loads(res.data.decode())
		self.assertEqual(result.status_code, 401)
		self.assertEqual(result['message'], "Login unsuccessful. Please register or confirm details.")

	def tearDown(self):
		"""
		Delete all initialized variables
		"""
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()



