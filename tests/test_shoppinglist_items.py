import unittest
import json
from app import create_app, db

class ShoppingItemTestCase(unittest.TestCase):
	"""
	This class represents the shoppinglist items test case
	"""

	def register_user(self, username="test", email="test@gmail.com", password="testpass"):
		"""
		Helper method for registering users
		"""
		user_details = {
		'username' : username,
		'email' : email,
		'password' : password
		}
		return self.client().post('/auth/register', data=user_details)

	def login(self, username="test", email="test@gmail.com", password="password"):
		"""
		Helper method for logging in users
		"""
		user_details = {
		'username' : username,
		'email' : email,
		'password' : password
		}
		return self.client().post('/auth/login', data=user_details)

	def setUp(self):
		"""
		Initialize app, test client and test variables
		"""
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client
		self.shoppinglist = {'name': 'clothes'}
		self.shoppinglist_item = {'name': 'shirt', 'list_id': 1}

		with self.app.app_context():
			db.drop_all()
			db.create_all()

			# register and log in a user then create a shopping list
			self.register_user()
			result = self.login()
			access_token = json.loads(result.data.decode())['access_token']
			res = self.client().post(
				'/shoppinglists/',
				headers=dict(Authorization="Bearer " + access_token),
				data=self.shoppinglist)
			self.assertEqual(res.status_code, 201)

	def test_item_creation(self):
		"""
		Test whether API can create an item (POST request)
		"""
		res = self.client().post(
			'/shoppinglists/1/items',
			headers=dict(Authorization="Bearer " + self.access_token),
			data=self.shoppinglist_item)
		self.assertEqual(res.status_code, 201)
		self.assertIn('shirt', str(res.data))

	def test_get_item_by_id(self):
		"""
		Test whether API can get a single shoppinglist item created (GET request)
		"""
		res = self.client().post(
			'/shoppinglists/1/items',
			headers=dict(Authorization="Bearer " + self.access_token),
			data=self.shoppinglist_item)
		self.assertEqual(res.status_code, 201)
		results = json.loads(res.data.decode())
		result = self.client().get(
			'/shoppinglists/1/items/{}'.format(results['id']),
			headers=dict(Authorization="Bearer " + self.access_token),
			data=self.shoppinglist_item)
		self.assertEqual(result.status_code, 200)
		self.assertIn('shirt', str(result.data))

	def test_item_edit(self):
		"""
		Test whether API can update an item creates (PUT request)
		"""
		res = self.client().post('/shoppinglists/1/items',
			headers=dict(Authorization="Bearer " + self.access_token),
			data=self.shoppinglist_item)
		self.assertEqual(res.status_code, 201)
		results = json.loads(res.data.decode())

		second_res = self.client().put(
			'/shoppinglists/1/items/{}'.format(results['id']),
			headers=dict(Authorization="Bearer " + self.access_token),
			data={'name': 'trouser'})
		self.assertEqual(second_res.status_code, 201)

		third_res = self.client().get(
			'/shoppinglists/1/item/{}'.format(results['id']),
			headers=dict(Authorization="Bearer " + self.access_token))
		self.assertIn('trouser', str(second_res.data))

	def test_item_deletion(self):
		"""
		Test whether API can delete an item created (DELETE request)
		"""
		res = self.client().post('/shoppinglists/1/items',
			headers=dict(Authorization="Bearer " + self.access_token),
			data=self.shoppinglist_item)
		self.assertEqual(res.status_code, 201)
		results = json.loads(res.data.decode())

		result = self.client().delete(
			'/shoppinglists/1/items/{}'.format(results['id']),
			headers=dict(Authorization="Bearer " + self.access_token))
		self.assertEqual(result.status_code, 200)

		second_res = self.client().get(
			'/shoppinglists/1/items/{}'.format(results['id']),
			headers=dict(Authorization="Bearer " + self.access_token))
		self.assertEqual(second_res.status_code, 404)

	def tearDown(self):
		"""
		Delete all initialized variables
		"""
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()
