# -*- coding: utf-8 -*-

from __future__ import absolute_import
from snakebite.helpers.json_helper import json_loads


def get_json_data(req):
    return json_loads(req.stream.read())
