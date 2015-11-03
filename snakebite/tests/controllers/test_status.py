# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from falcon import testing

import mock
from snakebite.controllers import status
from snakebite.tests import get_mock_auth_middleware, get_test_snakebite


class TestRestaurantCollectionGet(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = status.Status()

        self.api.add_route('/status', self.resource)
        self.srmock = testing.StartResponseMock()

    def tearDown(self):
        pass

    def test_status_on_get(self):

        res = self.simulate_request('/status', method='GET', headers={'accept': 'application/json'})
        self.assertTrue(isinstance(res, list))
        body = json.loads(res[0])
        self.assertDictEqual(body, {'ok': True})
