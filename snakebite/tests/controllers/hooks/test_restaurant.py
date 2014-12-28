# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.controllers import restaurant
import json


class TestRestaurantCollection(testing.TestBase):

    def before(self):
        self.resource = restaurant.Collection()
        self.api.add_route('/restaurants', self.resource)

    def test_collection_on_get(self):

        tests = [
            {'query_string': 'a=1&b=2', 'expected': {"a": "1", "b": "2"}},
            {'query_string': 'a=1,2,3,4,5', 'expected': {"a": "1,2,3,4,5"}}
        ]

        for t in tests:
            res = self.simulate_request('/restaurants',
                                        query_string=t['query_string'],
                                        method='GET',
                                        headers={'accept': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))
            self.assertDictEqual(body, t['expected'])

    def test_collection_on_post(self):

        tests = [
            {
                'data': '{"name": "KFC", "address": "ueno"}',
                'expected': {"name": "KFC", "address": "ueno", "description": "", "email": "", "tags": []}
            },
            {
                'data': '{"name": "KFC", "address": "ueno", "tags": "a,b,c"}',
                'expected': {"name": "KFC", "address": "ueno", "description": "", "email": "", "tags": ["a", "b", "c"]}
            },
            {
                'data': '{"name": "KFC", "address": "ueno", "description": "KFC desu", "email": "", "tags": "a,b,c"}',
                'expected': {"name": "KFC", "address": "ueno", "description": "KFC desu", "email": "", "tags": ["a", "b", "c"]}
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
            self.assertDictEqual(body, t['expected'])
