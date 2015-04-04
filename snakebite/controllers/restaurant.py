# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
from snakebite import constants
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.controllers.schema.restaurant import RestaurantSchema, RestaurantCreateSchema
from snakebite.models.restaurant import Restaurant, Menu
from snakebite.libs.error import HTTPBadRequest
from snakebite.helpers.geolocation import reformat_geolocations_map_to_list, reformat_geolocations_point_field_to_map
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned, ValidationError


# -------- BEFORE_HOOK functions
def deserialize_create(req, res, resource):
    deserialize(req, res, resource, schema=RestaurantCreateSchema())
    req.params['body'] = reformat_geolocations_map_to_list(req.params['body'], ['geolocation'])


def deserialize_update(req, res, id, resource):
    deserialize(req, res, resource, schema=RestaurantSchema())
    req.params['body'] = reformat_geolocations_map_to_list(req.params['body'], ['geolocation'])

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
        # custom filters
        # temp dict for updating query filters
        updated_params = {}

        for item in ['name', 'description']:
            if item in query_params:
                item_val = query_params.pop(item)
                updated_params['{}__icontains'.format(item)] = item_val

        try:
            if 'geolocation' in query_params:
                geolocation_val = query_params.pop('geolocation')
                geolocation_val = map(float, geolocation_val.split(',')[:2])
                max_distance = int(query_params.pop('maxDistance', constants.MAX_DISTANCE_SEARCH))

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
        for r in restaurants:
            reformat_geolocations_point_field_to_map(r, 'geolocation')

        res.body = {'items': restaurants, 'count': len(restaurants)}


    @falcon.before(deserialize_create)
    @falcon.after(serialize)
    def on_post(self, req, res):
        # save restaurants, and menus (if any)
        data = req.params.get('body')  # restaurant data
        menu_data = data.pop('menus')

        # save to DB
        restaurant = Restaurant(**data)
        restaurant.save()
        menus = []
        for mdata in menu_data:
          mdata.update({'restaurant': restaurant})
          menus.append(Menu(**mdata))  # extract info meant for menus

        Menu.objects.insert(menus)

        # return Restaurant (no menus)
        restaurant = Restaurant.objects.get(id=restaurant.id)
        res.body = restaurant
        res.body = reformat_geolocations_point_field_to_map(res.body, 'geolocation')


class Item(object):
    def __init__(self):
        pass

    def _try_get_restaurant(self, id):
        try:
            return Restaurant.objects.get(id=id)
        except (ValidationError, DoesNotExist, MultipleObjectsReturned) as e:
            raise HTTPBadRequest(title='Invalid Value', description='Invalid ID provided. {}'.format(e.message))

    @falcon.after(serialize)
    def on_get(self, req, res, id):
        restaurant = self._try_get_restaurant(id)
        res.body = reformat_geolocations_point_field_to_map(restaurant, 'geolocation')


    @falcon.after(serialize)
    def on_delete(self, req, res, id):
        restaurant = self._try_get_restaurant(id)
        restaurant.delete()

    # TODO: handle PUT requests
    @falcon.before(deserialize_update)
    @falcon.after(serialize)
    def on_put(self, req, res, id):
        restaurant = self._try_get_restaurant(id)
        data = req.params.get('body')

        # save to DB
        for key, value in data.iteritems():
            setattr(restaurant, key, value)
        restaurant.save()

        restaurant = Restaurant.objects.get(id=id)
        res.body = restaurant
        res.body = reformat_geolocations_point_field_to_map(res.body, 'geolocation')
