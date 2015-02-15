# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.tests import get_test_snakebite
from snakebite.controllers import status
from snakebite.libs.error import HTTPServiceUnavailable
import json
import mock


class TestRestaurantCollectionGet(testing.TestBase):

    def setUp(self):
        self.resource = status.Status()
        self.api = get_test_snakebite().app

        self.api.add_route('/status', self.resource)
        self.srmock = testing.StartResponseMock()

    def tearDown(self):
        pass

    def test_status_on_get(self):

        res = self.simulate_request('/status', method='GET', headers={'accept': 'application/json'})
        self.assertTrue(isinstance(res, list))
        body = json.loads(res[0])
        self.assertDictEqual(body, {'ok': True})
