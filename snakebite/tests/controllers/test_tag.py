# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

import mock
from falcon import testing

from snakebite.controllers import tag
from snakebite.models.restaurant import Menu
from snakebite.tests import get_mock_auth_middleware, get_test_snakebite


class TestRestaurantCollectionGet(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = tag.Collection()
        self.api.add_route('/tags', self.resource)
        self.srmock = testing.StartResponseMock()
        self.tags = ['buzzword', 'hipster', 'trending', 'barely trending', 'classic', 'safe', 'weird', 'regrettable']

        for i in range(len(self.tags)):
            r = Menu(name='Menu #{}'.format(i), price=200.00, currency='JPY', images=['http://example.com/1.jpg'],
                     tags=[])
            r.tags = self.tags[:-i] if i else self.tags  # first restaurant has more tags than the next
            r.save()

    def tearDown(self):
        Menu.objects.delete()

    def test_collection_on_get(self):

        tags = self.tags

        tests = [
            {'query_string': '', 'expected': {"status": 200, "count": len(tags), "tags": tags}},
            {'query_string': 'limit=3', 'expected': {"status": 200, "count": 3, "tags": tags[:3]}},
            {'query_string': 'start=3&limit=4', 'expected': {"status": 200, "count": 4, "tags": tags[3:3 + 4]}},
            {'query_string': 'start=1limit=1', 'expected': {"status": 400}}
        ]
        for t in tests:
            res = self.simulate_request('/tags',
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
            self.assertEqual(body['count'], t['expected']['count'])
            result_tags = [tag[0] for tag in body['items']]
            self.assertItemsEqual(result_tags, t['expected']['tags'])
