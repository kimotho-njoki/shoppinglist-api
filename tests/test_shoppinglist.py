import unittest
import json
from app import *

class ShoppinglistTestCase(unittest.TestCase):
	"""
	This class represents the shoppinglist test case
	"""

	def setUp(self):
		"""
		Initialise app, test client and test variables
		"""
		self.app = create_app(config_name='testing')
		self.client = self.app.test_client
		self.shoppinglist = {'name':'clothes'}

		with self.app.app_context():
			db.drop_all()
			db.create_all()

	def test_shoppinglist_creation(self):
		"""
		Test whether API can create a shoppinglist (POST request)
		"""
		res = self.client().post('/shoppinglists/', data=self.shoppinglist)
		self.assertEqual(res.status_code, 201)
		self.assertIn('clothes', str(res.data))

	def test_read_all_shoppinglists(self):
		"""
		Test whether API can get all shoppinglists created (GET request)
		"""
		res = self.client().post('/shoppinglists/', data=self.shoppinglist)
		self.assertEqual(res.status_code, 201)
		res = self.client().get('/shoppinglists/', data=self.shoppinglist)
		self.assertEqual(res.status_code, 200)
		self.assertIn('clothes', str(res.data))

	def test_read_one_shoppinglist(self):
		"""
		Test whether API can get shoppinglist by id (GET request)
		"""
		res = self.client().post('/shoppinglists/', data=self.shoppinglist)
		self.assertEqual(res.status_code, 201)
		result_in_json = json.loads(res.data.decode())
		result = self.client().get('/shoppinglists/{}', format(result_in_json['id']))
		self.assertEqual(result.status_code, 200)
		self.assertIn('clothes', str(result.data))

	def test_shoppinglist_editing(self):
		"""
		Test whether API can update an existing shopping list (PUT request)
		"""
		res = self.client().post('/shoppinglists/', data={'name':'grocery'})
		self.assertEqual(res.status_code, 201)
		res = self.client().put('/shoppinglists/1', data={'name':'books'})
		self.assertEqual(res.status_code, 200)
		result = self.client().get('/shoppinglists/1')
		self.assertIn('books', str(result.data))

	def test_shoppinglist_deletion(self):
		"""
		Test whether API can delete an existing shopping list (DELETE request)
		"""
		rv = self.client().post('/shoppinglists/', data={'name':'school'})
		self.assertEqual(rv.status_code, 201)
		res = self.client().delete('/shoppinglists/1')
		self.assertEqual(res.status_code, 200)
		result = self.client().get('/shoppinglists/1')
		self.assertEqual(result.status_code, 404)

	def tearDown(self):
		"""
		Delete all initialized variables
		"""
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()
