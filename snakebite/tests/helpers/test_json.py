# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest
from snakebite.helpers.json import map_query


class TestJson(unittest.TestCase):

    def test_map_query(self):
        tests = [
            {'query': 'a=A', 'expected': {'a': 'A'}},
            {'query': 'a=1&b=2&c=3', 'expected': {'a': '1', 'b': '2', 'c': '3'}},
            {'query': '', 'expected': {}},
            {'query': 'a=A|b=B=C', 'delim': '|', 'expected': {'a': 'A', 'b': 'B'}}
        ]

        for t in tests:
            result = map_query(t['query'], delim=t.get('delim', '&'))
            self.assertDictEqual(result, t['expected'])
