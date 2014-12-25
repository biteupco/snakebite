# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest
import colander
import mock
from snakebite.helpers.schema import CommaList, CommaIntList

dummy = mock.Mock()


class TestCommaList(unittest.TestCase):

    def test_deserialize(self):
        tests = [
            {'cstruct': colander.null, 'expected': []},
            {'cstruct': '', 'expected': []},
            {'cstruct': ' a , b , c , d , e ', 'expected': ['a', 'b', 'c', 'd', 'e']}
        ]
        comma_list = CommaList()
        for t in tests:
            result = comma_list.deserialize(None, t['cstruct'])
            self.assertEqual(result, t['expected'])


class TestCommaIntList(unittest.TestCase):

    def test_deserialize(self):
        tests = [
            {'cstruct': colander.null, 'expected': []},
            {'cstruct': '', 'expected': []},
            {'cstruct': ' 1 , 2 , 3 , 4 , 5 ', 'expected': range(1, 6)}
        ]
        comma_int_list = CommaIntList()
        for test in tests:
            result = comma_int_list.deserialize(dummy, test['cstruct'])
            self.assertEqual(result, test['expected'])

    def test_is_int_list(self):
        tests = [
            {'list': colander.null, 'error': True},
            {'list': [1, 'c'], 'error': True},
            {'list': range(10), 'error': False},
            {'list': CommaIntList().deserialize(dummy, ' 24, 7 '), 'error': False}
        ]

        for t in tests:
            if t['error']:
                self.assertRaises(Exception, CommaIntList.is_int_list, dummy, t['list'])
            else:
                self.assertIsNone(CommaIntList.is_int_list(dummy, t['list']))  # passes validation
