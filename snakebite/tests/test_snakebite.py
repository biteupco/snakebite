# -*- coding: utf-8 -*-

from __future__ import absolute_import


import json
import logging
import os

from falcon import testing

import jwt

import mock

from snakebite import constants
from snakebite.controllers import status
from snakebite.models.user import Role, User
from snakebite.tests import get_test_snakebite


class TestMain(testing.TestBase):

    def setUp(self):
        logging.disable(logging.INFO)
        test_snakebite = get_test_snakebite()
        self.api = test_snakebite.app
        self.config = test_snakebite.config
        self.db = test_snakebite.db

    def test_db(self):
        self.assertIsNotNone(self.db)

    def test_config(self):
        # list out important sections and options in config files that should be loaded
        tests = [
            {'section': 'cors', 'options': ['allowed_origins', 'allowed_headers']},
            {'section': 'mongodb', 'options': ['name', 'host', 'port']},
            {'section': 'logging', 'options': ['level']}
        ]

        for t in tests:
            section = t['section']
            for option in t['options']:
                self.assertIn(option, self.config[section])


class TestCorsMiddlewares(testing.TestBase):

    def test_cors(self):

        def _prepare():
            mock_cors_dict = {
                'allowed_origins': 'http://benri.com:5000,http://google.com',
                'allowed_headers': 'Content-Type',
                'allowed_methods': 'GET,PUT,POST,DELETE,OPTIONS'
            }

            snakebite = get_test_snakebite()
            snakebite.config = {'cors': mock_cors_dict}
            return snakebite.cors_middleware()

        cors_middleware = _prepare()
        dummy = mock.Mock()
        req = mock.Mock()

        tests = [
            {'origin': 'http://benri.com:5000', 'allowed': True},
            {'origin': 'http://benri.com:6000', 'allowed': False},
            {'origin': 'http://google.com', 'allowed': True},
            {'origin': 'http://mylittlepony.com', 'allowed': False},
        ]

        for t in tests:
            req.get_header.return_value = t['origin']
            res = mock.Mock()
            res.headers = {}

            def set_mock_header(dct):
                res.headers.update(dct)

            res.set_headers = set_mock_header
            cors_middleware(req, res, dummy)

            if t['allowed']:
                self.assertIn('Access-Control-Allow-Origin', res.headers)
            else:
                self.assertNotIn('Access-Control-Allow-Origin', res.headers)


class TestAuthMiddleware(testing.TestBase):
    def setUp(self):
        self.api = get_test_snakebite().app
        self.resource = status.Status()
        self.api.add_route('/status', self.resource)
        self.srmock = testing.StartResponseMock()

        users = [
            User(first_name='Clarke', last_name='Kent', display_name='Clarke Kent', email='superman@gmail.com', role=Role.USER)
        ]
        self.users = []
        for user in users:
            user.save()
            self.users.append(user)

    def tearDown(self):
        User.objects.delete()

    def test_jwt_auth_middleware(self):
        tests = [
            {
                'desc': 'success',
                'payload': {'sub': str(self.users[0].id), 'iss': constants.AUTH_SERVER_NAME, 'acl': 'admin'},
                'secret': os.getenv(constants.AUTH_SHARED_SECRET_ENV),
                'expected': {'status': 200}
            },
            {
                'desc': 'missing jwt params',
                'expected': {'status': 401}
            },
            {
                'desc': 'wrong secret',
                'payload': {'sub': str(self.users[0].id), 'iss': constants.AUTH_SERVER_NAME, 'acl': 'admin'},
                'secret': 'hush hush',
                'expected': {'status': 401}
            },
            {
                'desc': 'wrong iss',
                'payload': {'sub': str(self.users[0].id), 'iss': 'butler', 'acl': 'admin'},
                'secret': os.getenv(constants.AUTH_SHARED_SECRET_ENV),
                'expected': {'status': 401}
            },
            {
                'desc': 'missing values',
                'payload': {'iss': 'butler'},
                'secret': os.getenv(constants.AUTH_SHARED_SECRET_ENV),
                'expected': {'status': 401}
            },
            {
                'desc': 'invalid user id',
                'payload': {'sub': 'whosyourdaddy', 'iss': constants.AUTH_SERVER_NAME, 'acl': 'admin'},
                'secret': os.getenv(constants.AUTH_SHARED_SECRET_ENV),
                'expected': {'status': 401}
            }
        ]

        for test in tests:
            payload = test.get('payload')
            token = jwt.encode(payload, test['secret']) if payload else None
            qs = 'token={}'.format(token) if token else None

            res = self.simulate_request('/status',
                                        query_string=qs,
                                        method='GET',
                                        headers={'accept': 'application/json'})

            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if test['expected']['status'] != 200:
                self.assertEqual(body['title'], "Authorization Failed")
            else:
                self.assertEqual(body, {'ok': True})
