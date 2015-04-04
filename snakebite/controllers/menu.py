# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
from snakebite import constants
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.controllers.schema.restaurant import MenuSchema, MenuCreateSchema
from snakebite.models.restaurant import Menu, Restaurant
from snakebite.libs.error import HTTPBadRequest
from snakebite.helpers.range import min_max
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned, ValidationError


# -------- BEFORE_HOOK functions
def deserialize_create(req, res, resource):
    deserialize(req, res, resource, schema=MenuCreateSchema())


def deserialize_update(req, res, id, resource):
    deserialize(req, res, resource, schema=MenuSchema())


# -------- END functions

logger = logging.getLogger(__name__)


class Collection(object):
    def __init__(self):
        pass

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res):
        query_params = req.params.get('query')

        try:
            # get pagination limits
            start = int(query_params.pop('start', 0))
            limit = int(query_params.pop('limit', constants.PAGE_LIMIT))
            end = start + limit

        except ValueError as e:
            raise HTTPBadRequest(title='Invalid Value',
                                 description='Invalid arguments in URL query:\n{}'.format(e.message))

        # for convenience, we allow users to search for menus by their restaurant's geolocation too
        restaurants = list()
        try:
            if 'geolocation' in query_params:
                geolocation_val = query_params.pop('geolocation')
                geolocation_val = map(float, geolocation_val.split(',')[:2])
                max_distance = int(query_params.pop('maxDistance', constants.MAX_DISTANCE_SEARCH))

                # we deal with geolocation query in raw instead due to mongoengine bugs
                # see https://github.com/MongoEngine/mongoengine/issues/795
                # dated: 3/1/2015

                restuarant_query_params = {
                    '__raw__': {
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
                }
                # return list of restaurants satisfying geolocation requirements
                restaurants = Restaurant.objects(**restuarant_query_params)

        except Exception:
            raise HTTPBadRequest('Invalid Value', 'geolocation supplied is invalid: {}'.format(geolocation_val))

        # custom filters
        # temp dict for updating query filters
        updated_params = {}

        for item in ['name']:
            if item in query_params:
                item_val = query_params.pop(item)
                updated_params['{}__icontains'.format(item)] = item_val

        # skip updating query_params for filters on list fields like tags,
        # since mongoengine filters directly by finding any Menu that has tags of that value
        # e.g., GET /menu?tags=chicken returns all restaurants having 'chicken' tag

        if 'price' in query_params:
            price_range = query_params.pop('price')
            price_min, price_max = min_max(price_range, type='float')
            updated_params['price__gte'] = price_min
            updated_params['price__lte'] = price_max

        if restaurants:
            # we found nearby restaurants, filter menus further to menus from these restaurants only
            updated_params['__raw__'] = {
                "restaurant.$id": {
                    "$in": [r.id for r in restaurants]
                }
            }

        query_params.update(updated_params)  # update modified params for filtering
        menus = Menu.objects(**query_params)[start:end]

        res.body = {'items': menus, 'count': len(menus)}


    @falcon.before(deserialize_create)
    @falcon.after(serialize)
    def on_post(self, req, res):
        data = req.params.get('body')

        # save to DB
        restaurant_id = data.pop('restaurant_id')
        restaurant = Restaurant.objects.get(id=restaurant_id)

        data.update({'restaurant': restaurant})
        menu = Menu(**data)

        menu.save()

        menu = Menu.objects.get(id=menu.id)
        res.body = menu


class Item(object):
    def __init__(self):
        pass

    def _try_get_menu(self, id):
        try:
            return Menu.objects.get(id=id)
        except (ValidationError, DoesNotExist, MultipleObjectsReturned) as e:
            raise HTTPBadRequest(title='Invalid Value', description='Invalid ID provided. {}'.format(e.message))

    @falcon.after(serialize)
    def on_get(self, req, res, id):
        menu = self._try_get_menu(id)
        res.body = menu


    @falcon.after(serialize)
    def on_delete(self, req, res, id):
        menu = self._try_get_menu(id)
        menu.delete()

    # TODO: handle PUT requests
    @falcon.before(deserialize_update)
    @falcon.after(serialize)
    def on_put(self, req, res, id):
        menu = self._try_get_menu(id)
        data = req.params.get('body')

        # save to DB
        for key, value in data.iteritems():
            setattr(menu, key, value)
        menu.save()

        menu = Menu.objects.get(id=id)
        res.body = menu
