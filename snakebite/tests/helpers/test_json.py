# -*- coding: utf-8 -*-

from __future__ import absolute_import

from falcon import testing

from snakebite.helpers.json import map_query


class TestJson(testing.TestBase):

    def test_map_query(self):
        tests = [
            {'query': 'a=A', 'expected': {'a': 'A'}},
            {'query': 'a=1&b=2&c=3', 'expected': {'a': '1', 'b': '2', 'c': '3'}},
            {'query': '', 'expected': {}},
            {'query': 'a=A&b=B&b=C', 'delim': '|', 'expected': {'a': 'A', 'b': ['B', 'C']}}
        ]

        for t in tests:
            result = map_query(t['query'])
            self.assertDictEqual(result, t['expected'])
