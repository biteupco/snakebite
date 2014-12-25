# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
from snakebite.helpers.json_helper import jsonify
from snakebite.controllers.hooks.restaurant import validate_create_restaurant


class Restaurant(object):
    def __init__(self):
        pass

    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = jsonify({'test': 'example'})

    @falcon.before(validate_create_restaurant)
    def on_post(self, req, res):
        res.status = falcon.HTTP_200
        res.body = jsonify(req.params['data'])
