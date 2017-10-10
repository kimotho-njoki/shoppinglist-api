import unittest
import json
from app import *

class ShoppingItemTestCase(unittest.TestCase):
    """
    This class represents the shoppinglist items test case
    """
    def setUp(self):
        """
        Initialize app, test client and test variables
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shoppinglist = {'name': 'clothes'}
        self.shoppinglist_item = {'name': 'shirt', 'budgeted_amount': 100, 'list_id': 1}

        with self.app.app_context():
            # db.drop_all()
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
        
    def test_item_creation(self):
        """
        Test whether API can create an item (POST request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)      
        res = self.client().post(
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 201)
        self.assertIn('shirt', str(res.data))

    def test_item_creation_twice(self):
        """
        Test whether API can create the same item twice (POST request)
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
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(second_res.status_code, 201)
        third_res = self.client().post(
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(third_res.status_code, 302)

    def test_no_name_item_creation(self):
        """
        Test whether API can take a blank name field (POST request)
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
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': '', 'budgeted_amount': 100})
        self.assertIn('enter a name', str(second_res.data))


    def test_search_existing_item(self):
        """
        Test whether API can search for an item (GET request)
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
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(second_res.status_code, 201)     
        res = self.client().get(
            '/shoppinglists/1/items?q=shi',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 200)
        self.assertIn('shirt', str(res.data))

    def test_search_nonexisting_item(self):
        """
        Test whether API can search for an non existing item (GET request)
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
            '/shoppinglists/1/items?q=kerchief',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 404)

    def test_correct_page_no(self):
        """
        Test whether API can take a correct page no (GET request)
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
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(second_res.status_code, 201)           
        res = self.client().get(
            '/shoppinglists/1/items?limit=1&page=1',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 200)

    def test_incorrect_page_no(self):
        """
        Test whether API can take an incorrect page no (GET request)
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
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(second_res.status_code, 201)           
        res = self.client().get(
            '/shoppinglists/1/items?limit=1&page=one',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertIn('must be an integer', str(res.data))

    def test_correct_limit(self):
        """
        Test whether API can take a correct limit no
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
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(second_res.status_code, 201)           
        res = self.client().get(
            '/shoppinglists/1/items?limit=1&page=1',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 200)

    def test_incorrect_limit_no(self):
        """
        Test whether API can take an incorrect limit no
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
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(second_res.status_code, 201)           
        res = self.client().get(
            '/shoppinglists/1/items?limit=one&page=1',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertIn('must be an integer', str(res.data))
       
    def test_get_all_items(self):
        """
        Test whether API can get all items created (GET request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 200)

    def test_get_item_by_id(self):
        """
        Test whether API can get a single shoppinglist item created (GET request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        result = self.client().get(
            '/shoppinglists/1/items/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(result.status_code, 200)
        self.assertIn('shirt', str(result.data))

    def test_item_edit(self):
        """
        Test whether API can update an item creates (PUT request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        second_res = self.client().put(
            '/shoppinglists/1/items/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'trouser', 'budgeted_amount': 200})
        self.assertEqual(second_res.status_code, 200)

        third_res = self.client().get(
            '/shoppinglists/1/items/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('trouser', str(second_res.data))

    def test_item_deletion(self):
        """
        Test whether API can delete an item created (DELETE request)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/items',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.shoppinglist_item)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())

        result = self.client().delete(
            '/shoppinglists/1/items/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)

        second_res = self.client().get(
            '/shoppinglists/1/items/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
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
