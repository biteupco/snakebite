# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
from snakebite import constants
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.models.restaurant import Menu
from snakebite.models.rating import MenuRating
from snakebite.libs.error import HTTPBadRequest
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned, ValidationError


class Collection(object):
    def __init__(self):
        pass

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res):
        """
        Search for user's Menu ratings based on supplied user
        Only allows for searching by user
        """
        query_params = req.params.get('query')

        try:
            # get pagination limits
            start = int(query_params.pop('start', 0))
            limit = int(query_params.pop('limit', constants.PAGE_LIMIT))
            end = start + limit

        except ValueError as e:
            raise HTTPBadRequest(title='Invalid Value',
                                 description='Invalid arguments in URL query:\n{}'.format(e.message))

        user_id = query_params.pop('user_id')
        if not user_id:
            raise HTTPBadRequest(title='Invalid Request',
                                 description='Please supply a user ID in the query params')

        updated_params = {'__raw__': {'user.$id': user_id}}

        ratings = MenuRating.objects(**updated_params)[start:end]
        res.body = {'items': ratings, 'count': len(ratings)}


class Item(object):
    def __init__(self):
        pass

    def _try_get_menu(self, id):
        try:
            return Menu.objects.get(id=id)
        except (ValidationError, DoesNotExist, MultipleObjectsReturned) as e:
            raise HTTPBadRequest(title='Invalid Value', description='Invalid ID provided. {}'.format(e.message))

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res, id):


        menu = self._try_get_menu(id)
        ratings = MenuRating.objects(menu=menu)
        res.body = {'items': ratings, 'count': len(ratings)}
