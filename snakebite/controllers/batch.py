# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

import falcon
from mongoengine.errors import (DoesNotExist, MultipleObjectsReturned,
                                ValidationError)

from snakebite.controllers.hooks import deserialize, serialize
from snakebite.helpers.geolocation import \
    reformat_geolocations_point_field_to_map
from snakebite.libs.error import HTTPBadRequest
from snakebite.models.restaurant import Restaurant

logger = logging.getLogger(__name__)


class RestaurantCollection(object):
    def __init__(self):
        pass

    def _try_get_restaurant(self, id):
        try:
            return Restaurant.objects.get(id=id)
        except (ValidationError, DoesNotExist, MultipleObjectsReturned) as e:
            raise HTTPBadRequest(title='Invalid Value', description='Invalid ID provided. {}'.format(e.message))

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res):
        query_params = req.params.get('query')

        # get IDs
        try:
            ids = query_params.pop('ids')
        except KeyError:
            raise HTTPBadRequest(title='Invalid Request',
                                 description='Missing ID parameter in URL query')

        # parse IDs
        ids = ids.split(',')
        restaurants = []
        for id in ids:
            restaurant = self._try_get_restaurant(id)
            reformat_geolocations_point_field_to_map(restaurant, 'geolocation')
            restaurants.append(restaurant)

        res.body = {'items': restaurants, 'count': len(restaurants)}
