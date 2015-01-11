# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.controllers.schema.restaurant import RestaurantSchema
from snakebite.models.restaurant import Restaurant, Menu
from snakebite.libs.error import HTTPBadRequest
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned


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

        # get pagination limits
        start = int(query_params.pop('start', 0))
        limit = int(query_params.pop('limit', 20))
        end = start + limit

        # temp dict for updating query filters
        updated_params = {}

        for item in ['name', 'description', 'menus.name']:
            if item in query_params:
                item_val = query_params.pop(item)
                updated_params['{}__icontains'.format(item)] = item_val

        # skip updating query_params for filters on list fields like tags or menus.tags,
        # since mongoengine filters directly by finding any Restaurant that has tags of that value
        # e.g., GET /restaurants?tags=chicken returns all restaurants having 'chicken' tag

        try:
            if 'geolocation' in query_params:
                geolocation_val = query_params.pop('geolocation')
                geolocation_val = map(float, geolocation_val.split(',')[:2])
                
                max_distance = int(query_params.pop('maxDistance', 1000))  # defaulted to 1km

                # we deal with geolocation query in raw instead due to mongoengine bugs
                # see https://github.com/MongoEngine/mongoengine/issues/795
                # dated: 3/1/2015

                updated_params['__raw__'] = {
                    'geolocation': {
                        '$near': {
                            '$geometry': {
                                'type': 'Point',
                                'coordinates': geolocation_val
                            },
                            '$maxDistance': max_distance
                        },
                    }
                }

        except Exception:
            raise HTTPBadRequest('Invalid Value', 'geolocation supplied is invalid: {}'.format(geolocation_val))

        query_params.update(updated_params)  # update modified params for filtering

        restaurants = Restaurant.objects(**query_params)[start:end]
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
    def __init__(self):
        pass

    def _try_get_restaurant(self, id):
        try:
            return Restaurant.objects.get(id=id)
        except (DoesNotExist, MultipleObjectsReturned) as e:
            raise HTTPBadRequest(title='Invalid Value', description='Invalid ID provided. {}'.format(e.message))

    @falcon.after(serialize)
    def on_get(self, req, res, id):
        restaurant = self._try_get_restaurant(id)
        res.body = restaurant

    @falcon.after(serialize)
    def on_delete(self, req, res, id):
        restaurant = self._try_get_restaurant(id)
        restaurant.delete()

    # TODO: handle PUT requests
