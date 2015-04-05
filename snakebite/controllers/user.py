# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
from snakebite import constants
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.models.user import User
from snakebite.libs.error import HTTPBadRequest
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned, ValidationError


# -------- BEFORE_HOOK functions
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

        users = User.objects(**query_params)[start:end]
        res.body = {'items': users, 'count': len(users)}


class Item(object):
    def __init__(self):
        pass

    def _try_get_user(self, id):
        try:
            return User.objects.get(id=id)
        except (ValidationError, DoesNotExist, MultipleObjectsReturned) as e:
            raise HTTPBadRequest(title='Invalid Value', description='Invalid ID provided. {}'.format(e.message))

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res, id):
        user = self._try_get_user(id)
        res.body = user
