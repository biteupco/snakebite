# -*- coding: utf-8 -*-

from __future__ import absolute_import

import mock
from falcon import testing

from snakebite.helpers.geolocation import (reformat_geolocations_map_to_list,
                                           reformat_geolocations_point_field_to_map)


class TestGeolocation(testing.TestBase):

    def test_reformat_geolocations_map_to_list(self):
        tests = [
            {
                'dct': {},
                'attrs': [],
                'okay': True,
                'expected': {}
            },
            {
                'dct': {
                    'geolocation': {'lon': 12, 'lat': 23},
                    'name': 'test'
                },
                'attrs': 'geolocation',
                'okay': True,
                'expected': {
                    'name': 'test',
                    'geolocation': [12, 23]
                }
            },
            {
                'dct': {
                    'geolocation1': {'lon': 12, 'lat': 23},
                    'geolocation2': {'lon': 24, 'lat': 46}
                },
                'attrs': ['geolocation1', 'geolocation2'],
                'okay': True,
                'expected': {
                    'geolocation1': [12, 23],
                    'geolocation2': [24, 46]
                }
            },
            {
                'dct': {
                    'geolocation': {'lon': 12, 'lat': 23},
                },
                'attrs': 1234567,
                'okay': False
            },
            {
                'dct': {
                    'geolocation': {'lon': 12, 'lat': 23},
                },
                'attrs': 'locality',  # we did not select right attributes to reformat
                'okay': True,
                'expected': {
                    'geolocation': {'lon': 12, 'lat': 23}
                }
            },
        ]

        for t in tests:
            if t['okay']:
                result = reformat_geolocations_map_to_list(t['dct'], t['attrs'])
                self.assertDictEqual(result, t['expected'])
            else:
                self.assertRaises(Exception, reformat_geolocations_map_to_list, t['dct'], t['attrs'])

    def test_reformat_geolocations_point_field_to_map(self):

        def _create_dummy_obj(**kwargs):
            dummy = mock.Mock()
            for k, v in kwargs.iteritems():
                setattr(dummy, k, v)
            return dummy

        tests = [
            {
                'obj': _create_dummy_obj(),
                'attrs': [],
                'okay': True,
                'expected': _create_dummy_obj()
            },
            {
                'obj': mock.Mock(geolocation={'type': 'Point', 'coordinates': [1, 2]}),
                'attrs': ['geolocation'],
                'okay': True,
                'expected': mock.Mock(geolocation={'lon': 1, 'lat': 2})
            },
            {
                'obj': mock.Mock(geolocation={'type': 'Point', 'coordinates': [1, 2]}),
                'attrs': 123456.789,
                'okay': False
            },
            {
                'obj': mock.Mock(geolocation={'type': 'Point', 'description': 'should throw error'}),
                'attrs': ['geolocation'],
                'okay': True,
                'expected': mock.Mock(geolocation={'type': 'Point', 'description': 'should throw error'})
            }
        ]

        for t in tests:
            if t['okay']:
                result = reformat_geolocations_point_field_to_map(t['obj'], t['attrs'])
                for attr in t['attrs']:
                    self.assertDictEqual(getattr(result, attr), getattr(t['expected'], attr))
            else:
                self.assertRaises(Exception, reformat_geolocations_map_to_list, t['obj'], t['attrs'])
