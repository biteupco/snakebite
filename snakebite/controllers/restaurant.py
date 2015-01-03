# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.controllers.schema.restaurant import RestaurantSchema
from snakebite.models.restaurant import Restaurant, Menu


# -------- BEFORE_HOOK functions
def deserialize_create(req, res, resource):
    return deserialize(req, res, resource, schema=RestaurantSchema())

# -------- END functions

logger = logging.getLogger(__name__)


class Collection(object):
    def __init__(self):
        pass

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        query_params = req.params.get('query')

        # update query filters
        updated_params = {}

        for item in ['name', 'description', 'menus.name']:
            if item in query_params:
                item_val = query_params.pop(item)
                updated_params['{}__icontains'.format(item)] = item_val

        # TODO: filter by geolocation
        query_params.update(updated_params)

        restaurants = Restaurant.objects(**query_params)
        res.body = {'items': restaurants, 'count': len(restaurants)}

    @falcon.before(deserialize_create)
    @falcon.after(serialize)
    def on_post(self, req, res):
        res.status = falcon.HTTP_200
        data = req.params.get('body')

        # save to DB
        menu_data = data.pop('menus')  # extract info meant for menus

        restaurant = Restaurant(**data)
        restaurant.menus = [Menu(**menu) for menu in menu_data]

        restaurant.save()

        res.body = restaurant


class Item(object):
    pass
