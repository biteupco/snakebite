# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.controllers.schema.restaurant import CreateRestaurantSchema


# -------- BEFORE_HOOK functions
def deserialize_create(req, res, resource):
    return deserialize(req, res, resource, schema=CreateRestaurantSchema())

# -------- END functions

logger = logging.getLogger(__name__)


class Collection(object):
    def __init__(self):
        pass

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = req.params.get('query')

    @falcon.before(deserialize_create)
    @falcon.after(serialize)
    def on_post(self, req, res):
        res.status = falcon.HTTP_200
        res.body = req.params.get('body')


class Item(object):
    pass
