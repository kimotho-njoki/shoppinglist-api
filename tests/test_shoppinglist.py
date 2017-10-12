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
        self.user_details = {
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'testpass'}

        with self.app.app_context():
            db.create_all()

    def user_register_login(self):
        """
        Helper method to assist in registering users
        """
        self.client().post('/auth/register', data=self.user_details)
        resp = self.client().post('/auth/login', data=self.user_details)
        access_token = json.loads(resp.data.decode())['access_token']
        return access_token

    def test_shoppinglist_creation(self):
        """
        Test whether API can create a shoppinglist (POST request)
        """
        access_token = self.user_register_login()
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
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        second_res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(second_res.status_code, 302)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "Shoppinglist name already exists.")

    def test_no_name_shoppinglist_creation(self):
        """
        Test whether API can can take a blank name field (POST request)
        """
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': ''})
        self.assertIn('enter a name', str(res.data))

    def test_search_existing_shoppinglist(self):
        """
        Test whether API can search for a shoppinglist (GET request)
        """
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
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
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        res = self.client().get(
            '/shoppinglists/?q=product',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 404)

    def test_correct_page_no(self):
        """
        Test whether API can take a correct page no (GET request)
        """
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        res = self.client().get(
            '/shoppinglists/?limit=1&page=1',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 200)

    def test_incorrect_page_no(self):
        """
        Test whether API can take an incorrect page no (GET request)
        """
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        res = self.client().get(
            '/shoppinglists/?limit=1&page=ww',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertIn('must be an integer', str(res.data))

    def test_correct_limit_no(self):
        """
        Test whether API can take a correct limit no (GET request)
        """
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        res = self.client().get(
            '/shoppinglists/?limit=1&page=1',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 200)

    def test_incorrect_limit_no(self):
        """
        Test whether API can take an incorrect limit no (GET request)
        """
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        res = self.client().get(
            '/shoppinglists/?limit=one&page=1',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertIn('must be an integer', str(res.data))

    def test_read_all_shoppinglists(self):
        """
        Test whether API can get all shoppinglists created (GET request)
        """
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
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
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
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
        access_token = self.user_register_login()
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'grocery'})
        result_in_json = json.loads(res.data.decode())
        res = self.client().put(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'books'})
        result = self.client().get(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('books', str(result.data))

    def test_shoppinglist_deletion(self):
        """
        Test whether API can delete an existing shopping list (DELETE request)
        """
        access_token = self.user_register_login()
        rv = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name':'school'})
        result_in_json = json.loads(rv.data.decode())
        res = self.client().delete(
            '/shoppinglists/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token))
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
