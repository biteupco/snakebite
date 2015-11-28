# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

import mock
from falcon import testing

from snakebite.controllers import batch
from snakebite.models.restaurant import Restaurant
from snakebite.tests import get_mock_auth_middleware, get_test_snakebite


class TestBatchRestaurantCollectionGet(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = batch.RestaurantCollection()
        self.api.add_route('/batch/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()

        restaurants = [
            {
                'name': 'a',
                'description': 'desc A',
                'email': 'a@b.com',
                'address': 'tokyo',
            },
            {
                'name': 'b',
                'description': 'desc B',
                'email': 'b@a.com',
                'address': 'kyoto',
            }
        ]
        self.restaurants = []
        for r in restaurants:
            rest = Restaurant(**r)
            rest.save()
            self.restaurants.append(rest)

    def tearDown(self):
        Restaurant.objects(id__in=[r.id for r in self.restaurants]).delete()

    def test_on_get(self):

        tests = [
            {'query_string': '', 'expected': {'status': 400}},
            {'query_string': 'ids=', 'expected': {'status': 400}},
            {'query_string': 'ids=,,,,', 'expected': {'status': 400}},
            {'query_string': 'ids=invalid', 'expected': {'status': 400}},
            {'query_string': 'ids={}'.format(self.restaurants[0].id), 'expected': {'status': 200, 'count': 1}},
            {'query_string': 'ids={}'.format(",".join([str(r.id) for r in self.restaurants])), 'expected': {'status': 200, 'count': len(self.restaurants)}},
            {'query_string': 'ids={}&start=ignored'.format(",".join([str(r.id) for r in self.restaurants])), 'expected': {'status': 200, 'count': len(self.restaurants)}}
        ]

        for t in tests:
            res = self.simulate_request('/batch/restaurants',
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

            self.assertItemsEqual(["count", "items"], body.keys())
            got = body['count']
            want = t['expected']['count']
            self.assertEqual(got, want, "{}| got: {}, want: {}".format(t['query_string'], got, want))
