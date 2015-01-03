# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.tests import get_test_snakebite
from snakebite.controllers import restaurant
from snakebite.models.restaurant import Restaurant
from snakebite.constants import TOKYO_GEOLOCATION
import json


class TestRestaurantCollectionGet(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Collection()
        self.api = get_test_snakebite().app

        self.api.add_route('/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()
        self.restaurants = [
            Restaurant(name='a', description='desc', email='a@b.com', address='tokyo'),
            Restaurant(name='b', description='description', email='b@a.com', address='kyoto', tags=['b'])
        ]
        for r in self.restaurants:
            r.save()

    def tearDown(self):
        Restaurant.objects.delete()

    def test_collection_on_get(self):

        tests = [
            {'query_string': '', 'expected': {"count": 2}},
            {'query_string': 'description=description', 'expected': {"count": 1}},
            {'query_string': 'name=c', 'expected': {"count": 0}},
            {'query_string': 'email=b@a.com', 'expected': {"count": 1}}
        ]
        for t in tests:
            res = self.simulate_request('/restaurants',
                                        query_string=t['query_string'],
                                        method='GET',
                                        headers={'accept': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))
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
