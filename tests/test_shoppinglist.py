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
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shoppinglist = {'name': 'clothes'}

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def register_user(self, username="test", email="test@gmail.com", password="testpass"):
        """
        Helper method to assist in registering users
        """
        user_details = {
        'username': username,
        'email': email,
        'password': password
        }
        return self.client().post('/auth/register', data=user_details)

    def login_user(self, username="test", email="test@gmail.com", password="testpass"):
        """
        Helper method to assist in logging in users
        """
        user_details = {
        'username': username,
        'email': email,
        'password': password
        }
        return self.client().post('/auth/login', data=user_details)

    def test_shoppinglist_creation(self):
        """
        Test whether API can create a shoppinglist (POST request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('clothes', str(res.data))

    def test_shoppinglist_creation_twice(self):
        """
        Test whether API can create same shoppinglist twice (POST request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(second_res.status_code, 302)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "Shoppinglist name already exists.")

    def test_search_existing_shoppinglist(self):
        """
        Test whether API can search for a shoppinglist (GET request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/shoppinglists/?q=cloth',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 200)
        self.assertIn('clothes', str(res.data))

    def test_search_nonexisting_shoppinglist(self):
        """
        Test whether API can search for a nonexisting shoppinglist (GET request)
        """        
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/shoppinglists/?q=product',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 404)

    def test_read_all_shoppinglists(self):
        """
        Test whether API can get all shoppinglists created (GET request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 200)
        self.assertIn('clothes', str(res.data))

    def test_read_one_shoppinglist(self):
        """
        Test whether API can get shoppinglist by id (GET request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode())
        result = self.client().get(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('clothes', str(result.data))

    def test_shoppinglist_editing(self):
        """
        Test whether API can update an existing shopping list (PUT request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'grocery'})
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode())
        res = self.client().put(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'books'})
        self.assertEqual(res.status_code, 200)
        result = self.client().get(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('books', str(result.data))

    def test_shoppinglist_deletion(self):
        """
        Test whether API can delete an existing shopping list (DELETE request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'school'})
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode())
        res = self.client().delete(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        result = self.client().get(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
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
