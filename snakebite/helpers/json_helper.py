# -*- coding: utf-8 -*-

import json


def jsonify(dct):
    """returns a JSON object from a dict"""
    return json.dumps(dct, encoding='UTF-8')


def json_loads(str):
    return json.loads(str)
