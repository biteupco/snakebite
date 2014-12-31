# -*- coding: utf-8 -*-

from __future__ import absolute_import
from conf import get_config
from snakebite import create_snakebite


def get_test_snakebite():
    config = get_config('testing')
    return create_snakebite(**config)
