# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.controllers.schema.restaurant import CreateRestaurantSchema
from snakebite.models.restaurant import Restaurant


# -------- BEFORE_HOOK functions
def deserialize_create(req, res, resource):
    return deserialize(req, res, resource, schema=CreateRestaurantSchema())

# -------- END functions


class Collection(object):
    def __init__(self):
        pass

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        query_params = req.params.get('query')

        restaurants = Restaurant.objects(**query_params)
        res.body = {'items': restaurants, 'count': len(restaurants)}

    @falcon.before(deserialize_create)
    @falcon.after(serialize)
    def on_post(self, req, res):
        res.status = falcon.HTTP_200
        data = req.params.get('body')

        # save to DB
        restaurant = Restaurant(**data)
        restaurant.save()

        res.body = restaurant


class Item(object):
    pass
