# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from falcon import testing

import mock

from snakebite import constants
from snakebite.controllers import user
from snakebite.models.user import Role, User
from snakebite.tests import get_mock_auth_middleware, get_test_snakebite


class TestUserItemGet(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.controllers.user.request_user_satisfy'),\
             mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = user.Item()
        self.api.add_route('/users/{id}', self.resource)
        self.srmock = testing.StartResponseMock()

        self.users = [
            User(first_name='Clarke', last_name='Kent', display_name='Clarke Kent', email='a@b.com', role=Role.ADMIN),
            User(first_name='Bruce', last_name='Wayne', display_name='Bruce Wayne', email='bat@man.com', role=Role.EMPLOYEE)
        ]
        for u in self.users:
            u.save()

    def tearDown(self):
        User.objects(id__in=[u.id for u in self.users]).delete()

    def test_item_on_get(self):
        tests = [
            {
                'id': u.id,
                'expected': {
                    'status': 200,
                    'id': {
                        '_id': {
                            '$oid': str(u.id)
                        }
                    }
                }
            } for u in self.users
        ]

        for t in tests:
            res = self.simulate_request('/users/{}'.format(t['id']),
                                        method='GET',
                                        headers={'Content-Type': 'application/json', constants.AUTH_HEADER_USER_ID: t['id']})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if t['expected']['status'] != 200:
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())  # error

            else:
                self.assertDictContainsSubset(t['expected']['id'], body)
