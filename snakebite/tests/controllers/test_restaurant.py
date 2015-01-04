# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.tests import get_test_snakebite
from snakebite.controllers import restaurant
from snakebite.models.restaurant import Restaurant
from snakebite.constants import TOKYO_GEOLOCATION
from snakebite.libs.error import HTTPBadRequest
import json


class TestRestaurantCollectionGet(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Collection()
        self.api = get_test_snakebite().app

        self.api.add_route('/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()
        self.restaurants = [
            Restaurant(name='a', description='desc', email='a@b.com',
                       address='Asakusa, Taito-ku, Tokyo', tags=['x', 'y', 'z'], geolocation=[139.79843, 35.712074]),
            Restaurant(name='b', description='description', email='b@a.com',
                       address='Roppongi, Minato-ku, Tokyo', tags=['z'], geolocation=[139.731443, 35.662836])
        ]
        for r in self.restaurants:
            r.save()

    def tearDown(self):
        Restaurant.objects.delete()

    def test_collection_on_get(self):

        tests = [
            {'query_string': '', 'expected': {"status": 200, "count": 2}},
            {'query_string': 'description=desc', 'expected': {"status": 200, "count": 2}},
            {'query_string': 'description=description', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'name=c', 'expected': {"status": 200, "count": 0}},
            {'query_string': 'email=b@a.com', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'tags=z', 'expected': {"status": 200, "count": 2}},
            {'query_string': 'tags=x', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'tags=x&name=a', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'tags=x&name=c', 'expected': {"status": 200, "count": 0}},
            {'query_string': 'geolocation=139.731443,35.662836', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'geolocation=ab,cd', 'expected': {"status": 400}}
        ]
        for t in tests:
            res = self.simulate_request('/restaurants',
                                        query_string=t['query_string'],
                                        method='GET',
                                        headers={'accept': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if t['expected']['status'] != 200:  # expected erroneous requests
                self.assertNotIn('count', body.keys())
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())
                continue

            self.assertListEqual(["count", "items"], sorted(body.keys()))
            self.assertEqual(body['count'], t['expected']['count'], "{}".format(t['query_string']))


class TestRestaurantCollectionPost(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Collection()
        self.api = get_test_snakebite().app
        self.api.add_route('/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()

    def get_mock_restaurant(self, **kwargs):
        base_restaurant = {
            "name": "KFC",
            "address": "ueno",
            "email": "kf@c.com",
            "menus": [],
            "geolocation": TOKYO_GEOLOCATION
        }
        base_restaurant.update(kwargs)
        return base_restaurant

    def get_mock_menu(self, **kwargs):
        base_menu = {"name": "some menu", "price": 100.00, "currency": 'JPY', 'images': ['http://kfc.com/1.jpg']}
        base_menu.update(kwargs)
        return base_menu

    def tearDown(self):
        Restaurant.objects.delete()

    def test_collection_on_post(self):

        restaurant1 = self.get_mock_restaurant(name="First Kitchen")  # with no menus (not good!)

        restaurant2 = self.get_mock_restaurant()
        menus2 = [self.get_mock_menu(name="menu A"), self.get_mock_menu(name="menu B")]
        restaurant2.update({'menus': menus2})

        tests = [
            {
                'data': json.dumps(restaurant1),
                'expected': {
                    "name": "First Kitchen",
                    "address": "ueno",
                    "description": "",
                    "geolocation": {'type': 'Point', 'coordinates': list(TOKYO_GEOLOCATION)},
                    "email": "kf@c.com",
                    "tags": [],
                    "menus": []
                }
            },
            {
                'data': json.dumps(restaurant2),
                'expected': {
                    "name": "KFC",
                    "address": "ueno",
                    "description": "",
                    "geolocation": {'type': 'Point', 'coordinates': list(TOKYO_GEOLOCATION)},
                    "email": "kf@c.com",
                    "tags": [],
                    "menus": [
                        {
                            "name": "menu A",
                            "price": 100.00,
                            "currency": "JPY",
                            "tags": [],
                            "images": ['http://kfc.com/1.jpg'],
                            "rating": 0.0
                        },
                        {
                            "name": "menu B",
                            "price": 100.00,
                            "currency": "JPY",
                            "tags": [],
                            "images": ['http://kfc.com/1.jpg'],
                            "rating": 0.0
                        }
                    ]
                }
            }
        ]

        for t in tests:
            res = self.simulate_request('/restaurants',
                                        body=t['data'],
                                        method='POST',
                                        headers={'Content-Type': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))
            self.assertDictContainsSubset(t['expected'], body)
