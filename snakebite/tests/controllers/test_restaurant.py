# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.tests import get_test_snakebite
from snakebite.controllers import restaurant
from snakebite.models.restaurant import Restaurant
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

    def tearDown(self):
        Restaurant.objects.delete()

    def test_collection_on_post(self):

        tests = [
            {
                'data': '{"name": "KFC", "address": "ueno", "email": "kf@c.com"}',
                'expected': {"name": "KFC", "address": "ueno", "description": "",
                             "email": "kf@c.com", "tags": [], "geolocation": None}
            },
            {
                'data': '{"name": "KFC", "address": "ueno", "tags": "a,b,c", "email": "kf@c.com"}',
                'expected': {"name": "KFC", "address": "ueno", "description": "",
                             "email": "kf@c.com", "tags": ["a", "b", "c"], "geolocation": None}
            },
            {
                'data': '{"name": "KFC", "address": "ueno", "description": "KFC desu", '
                        '"email": "kf@c.com", "tags": "a,b,c"}',
                'expected': {"name": "KFC", "address": "ueno", "description": "KFC desu",
                             "email": "kf@c.com", "tags": ["a", "b", "c"], "geolocation": None}
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
