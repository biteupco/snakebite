# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
import mock
from snakebite import SnakeBite


class TestMain(testing.TestBase):

    def before(self):
        snakebite = SnakeBite()
        self.api = snakebite.app
        self.config = snakebite.config
        self.db = snakebite.db

    def test_db(self):
        self.assertIsNone(self.db)

    def test_config(self):
        # list out important sections and options in config files that should be loaded
        tests = [
            {'section': 'redis', 'options': ['db', 'host', 'port']},
            {'section': 'cors', 'options': ['allowed_origins', 'allowed_headers']}
        ]

        for t in tests:
            section = t['section']
            for option in t['options']:
                self.assertTrue(self.config.has_option(section, option), 'Missing Option: {0}'.format(option))


class TestMiddlewares(testing.TestBase):

    def test_cors_middleware(self):

        def _prepare():
            mock_config_parser = mock.Mock()
            mock_cors_dict = {
                'allowed_origins': 'http://benri.com:5000,http://google.com',
                'allowed_headers': 'Content-Type'
            }

            def get_cors_option(section, option):
                return mock_cors_dict[option]

            # mock config parser's get function
            mock_config_parser.get = get_cors_option

            snakebite = SnakeBite()
            snakebite.config = mock_config_parser
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
