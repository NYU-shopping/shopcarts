import unittest
import os
import json
import logging
from flask_api import status    # HTTP Status Codes

from app.models import Item
from app import server,db

DATABASE_URI = os.getenv('DATABASE_URI', None)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestItemServer(unittest.TestCase):
    """ Item Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        server.app.debug = False
        server.initialize_logging(logging.INFO)
        # Set up the test database
        server.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        server.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        Item(sku="ID111", count=3, price=2.00, name="test_item",
             link="test.com", brand_name="gucci", is_available=True).save()
        Item(sku="ID222", count=5, price=10.00, name="some_item",
             link="link.com", brand_name="nike", is_available=False).save()
        self.app = server.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/shopcarts')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_item_list(self):
        """ Get a list of Items """
        resp = self.app.get('/shopcarts/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_item(self):
        """ Get a single Item """
        # get the sku of an item
        item = Item.find_by_name('test_item')[0]
        resp = self.app.get('/shopcarts/items/{}'.format(item.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['sku'], item.sku)

    def test_get_item_not_found(self):
        """ Get an Item that's not found """
        resp = self.app.get('/shopcarts/items/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_item(self):
        """ Create a new Item """
        # save the current number of items for later comparison
        item_count = self.get_item_count()
        # add a new item
        new_item = {'sku': 'ID333', 'count': 5, 'price': 1000.00, 'name': 'watch', 'link': 'rolex.com',
                    'brand_name': 'rolex', 'is_available': True}
        data = json.dumps(new_item)
        resp = self.app.post('/shopcarts/items', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['sku'], 'ID333')
        # check that count has gone up and includes ID333
        resp = self.app.get('/shopcarts/items')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), item_count + 1)
        self.assertIn(new_json, data)

    def test_update_item(self):
        """ Update an existing Item """
        item = Item.find_by_sku('ID222')[0]
        new_id222 = {'sku': 'ID222', 'count': 5, 'price': 10.00, 'name': 'some_item', 'link': 'link.com',
                    'brand_name': 'reebok', 'is_available': False}
        data = json.dumps(new_id222)
        resp = self.app.put('/shopcarts/items/{}'.format(item.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['brand_name'], 'reebok')

    def test_delete_item(self):
        """ Delete an Item """
        item = Item.find_by_sku('ID111')[0]
        # save the current number of items for later comparison
        item_count = self.get_item_count()
        resp = self.app.delete('/shopcarts/items/{}'.format(item.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_item_count()
        self.assertEqual(new_count, item_count - 1)

    def test_delete_all_items(self):
        """ Delete all Items """
        resp = self.app.delete('/shopcarts/clear', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

    def test_query_item_list_by_brand(self):
        """ Query Items by Brand """
        resp = self.app.get('/shopcarts/items', query_string='brand_name=gucci')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('ID111', resp.data)
        self.assertNotIn('ID222', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['brand_name'], 'gucci')

    def test_query_item_list_by_name(self):
        """ Query Items by Name """
        resp = self.app.get('/shopcarts/items', query_string='name=test_item')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('ID111', resp.data)
        self.assertNotIn('ID222', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['name'], 'test_item')

    def test_query_item_list_by_sku(self):
        """ Query Items by Sku """
        resp = self.app.get('/shopcarts/items', query_string='sku=ID111')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('ID111', resp.data)
        self.assertNotIn('ID222', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['sku'], 'ID111')

    def test_update_item_not_found(self):
        """ Update an Item that doesn't exist """
        new_item = {"name": "jbkjb", "sku": "ID999"}
        data = json.dumps(new_item)
        resp = self.app.put('/shopcarts/items/0', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_item_with_no_name(self):
        """ Create an Item with only a sku """
        new_item = {'sku': 'ID555'}
        data = json.dumps(new_item)
        resp = self.app.post('/shopcarts/items', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_no_content_type(self):
        """ Create an Item with no Content-Type """
        new_item = {'sku': 'ID555'}
        data = json.dumps(new_item)
        resp = self.app.post('/shopcarts/items', data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexisting_item(self):
        """ Get a nonexisting Item """
        resp = self.app.get('/shopcarts/items/5')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_call_create_with_an_id(self):
        """ Call create passing an id """
        new_item = {'sku': "ID555", 'count': 4, 'price': 500.00, 'name': "bad_item",
             'link': "apple.com", 'brand_name': "apple", 'is_available': True}
        data = json.dumps(new_item)
        resp = self.app.post('/shopcarts/items/1', data=data)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_call_create_with_an_id(self):
        """ Call create passing an id """
        new_item = {'sku': "ID555", 'count': 4, 'price': 500.00, 'name': "bad_item",
             'link': "apple.com", 'brand_name': "apple", 'is_available': True}
        data = json.dumps(new_item)
        resp = self.app.post('/shopcarts/items/1', data=data)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

######################################################################
# Utility functions
######################################################################

    def get_item_count(self):
        """ save the current number of items """
        resp = self.app.get('/shopcarts/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
