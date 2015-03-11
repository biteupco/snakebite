# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
import mock
import logging
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


class TestMiddlewares(testing.TestBase):

    def test_cors_middleware(self):

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
