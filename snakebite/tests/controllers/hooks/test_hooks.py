# -*- coding: utf-8 -*-

from __future__ import absolute_import
import colander
import mock
from falcon import testing
from ast import literal_eval as eval
from snakebite.controllers.hooks import serialize, deserialize
from snakebite.libs.error import HTTPBadRequest, HTTPNotAcceptable

dummy = mock.Mock()


class MockSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    age = colander.SchemaNode(colander.Int())


class TestDeserialize(testing.TestBase):

    def test_deserialize(self):
        stream_tests = [
            {
                'method': 'POST',
                'stream': '{"name":"siri","age":"1"}',
                'schema': MockSchema(),
                'error': False,
                'expected': {'name': 'siri', 'age': 1}
            },
            {
                'method': 'POST',
                'stream': '{"name":"siri","weird_key":"!#$%&"}',
                'schema': MockSchema(),
                'error': True,
            },
        ]
        for t in stream_tests:
            req = mock.Mock()
            req.method = t['method']
            req.content_type = 'application/json'
            req.params = {}
            req.stream.read.return_value = t['stream']

            if t['error']:
                self.assertRaises(HTTPBadRequest, deserialize, req, dummy, dummy, schema=t['schema'])
            else:
                deserialize(req, dummy, dummy, schema=t['schema'])
                self.assertDictEqual(req.params['body'], t['expected'])

        query_tests = [
            {
                'method': 'GET',
                'query': 'a=b&c=d',
                'schema': None,
                'error': False,
                'expected': {'a': 'b', 'c': 'd'}
            },
            {
                'method': 'GET',
                'query': 'name=siri&age=1',
                'schema': MockSchema(),
                'error': False,
                'expected': {'name': 'siri', 'age': 1}
            },
            {
                'method': 'GET',
                'query': 'name=siri&wierd=OHNO',
                'schema': MockSchema(),
                'error': True,
            },
        ]
        for t in query_tests:
            req = mock.Mock()
            req.method = t['method']
            req.params = {}
            req.query_string = t['query']

            if t['error']:
                self.assertRaises(HTTPBadRequest, deserialize, req, dummy, dummy, schema=t['schema'])
            else:
                deserialize(req, dummy, dummy, schema=t['schema'])
                self.assertDictEqual(req.params['query'], t['expected'])

    def test_empty_stream(self):
        query_test = {'method': 'GET', 'query': '', 'expected': {}}

        req = mock.Mock()
        req.method = query_test['method']
        req.params = {}
        req.query_string = query_test['query']
        deserialize(req, dummy, dummy)
        self.assertEquals(req.params['query'], query_test['expected'])

        stream_test = {'method': 'POST', 'stream': '', 'expected': {}}

        req = mock.Mock()
        req.method = stream_test['method']
        req.content_type = 'application/json'
        req.params = {}
        req.stream.read.return_value = stream_test['stream']
        deserialize(req, dummy, dummy)
        self.assertEquals(req.params['body'], stream_test['expected'])

    def test_content_type_check(self):
        tests = [
            {'content_type': 'text/html', 'error': True},
            {'content_type': 'application/xml', 'error': True},
            {'content_type': 'application/gzip', 'error': True},
            {'content_type': 'application/json', 'error': False}
        ]

        for t in tests:

            req = mock.Mock()
            req.method = 'POST'
            req.content_type = t['content_type']
            req.params = {}
            req.stream.read.return_value = ""
            if t['error'] is True:
                self.assertRaises(HTTPNotAcceptable, deserialize, req, dummy, dummy)
            else:
                deserialize(req, dummy, dummy)
                self.assertEquals(req.params['body'], {})


class TestSerialize(testing.TestBase):

    def test_serialize(self):
        tests = [
            {'body': {}, 'expected': '{}'},
            {'body': {'name': 'siri', 'age': 1}, 'expected': '{"name": "siri", "age": 1}'}
            # TODO: deal with unicode
        ]
        for t in tests:
            resp = mock.Mock()
            resp.body = t['body']

            serialize(dummy, resp, dummy)
            self.assertDictEqual(eval(resp.body), eval(t['expected']))
