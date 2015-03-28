# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.helpers.range import min_max
from snakebite.constants import INTEGER_MAX


class Testrange(testing.TestBase):

    def test_min_max(self):
        tests = [
            {'range_str': '', 'expected': (0, INTEGER_MAX)},
            {'range_str': '', 'type': 'float', 'expected': (0.00, float(INTEGER_MAX))},
            {'range_str': '1,5', 'type': 'float', 'min': -1, 'max': 10, 'expected': (1.00, 5.00)},
            {'range_str': '10,-1', 'type': 'int', 'expected': (-1, 10)},
            {'range_str': '10,', 'type': 'int', 'expected': (10, INTEGER_MAX)},
            {'range_str': '2,10', 'type': 'str', 'expected': TypeError()}
        ]

        for test in tests:
            expected = test.pop('expected')
            if isinstance(expected, Exception):
                self.assertRaises(expected.__class__, min_max, **test)

            else:
                minmax = min_max(**test)
                self.assertEqual(minmax, expected)
