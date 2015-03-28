# -*- coding: utf-8 -*-

from __future__ import absolute_import
from snakebite.constants import INTEGER_MAX
import __builtin__


def min_max(range_str, type='int', delimiter=',', min=0, max=INTEGER_MAX):
    """
    Parses range_str and returns a tuple of (min, max) value
    Takes default of min or max if typecasting fails
    Hence, to get a returned min-max range of (0, 200), you can simply provide ',200'
    """
    accepted_types = ['int', 'float']
    if type not in accepted_types:
        raise TypeError("Please provide an accepted type: {}".format(accepted_types))

    numberize = getattr(__builtin__, type)

    r = range_str.split(delimiter)[:2]
    min_val = r[0]
    max_val = r[1] if len(r) > 1 else ''
    try:
        min_val = numberize(min_val)
    except ValueError:
        min_val = numberize(min)

    try:
        max_val = numberize(max_val)
    except ValueError:
        max_val = numberize(max)

    if min_val <= max_val:
        return (min_val, max_val)

    return (max_val, min_val)
