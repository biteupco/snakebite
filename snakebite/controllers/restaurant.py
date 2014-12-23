# -*- coding: utf-8 -*-

import falcon
from snakebite.helpers.json_helper import jsonify


class Restaurant(object):
    def __init__(self, app):
        app.add_route('/restuarants', self)

    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = jsonify({'test': 'example'})
