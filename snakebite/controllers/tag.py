# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
from operator import itemgetter
from snakebite.controllers.hooks import deserialize, serialize
from snakebite.models.restaurant import Menu
from snakebite.libs.error import HTTPBadRequest

logger = logging.getLogger(__name__)


class Collection(object):
    def __init__(self):
        pass

    @falcon.before(deserialize)
    @falcon.after(serialize)
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        query_params = req.params.get('query')

        try:
            # get pagination limits
            start = int(query_params.get('start', 0))
            limit = int(query_params.get('limit', 20))
            end = start + limit
        except ValueError as e:
            raise HTTPBadRequest(title='Invalid Value',
                                 description='Invalid arguments in URL query:\n{}'.format(e.message))

        tag_freqs = Menu.objects.item_frequencies('tags', normalize=True)
        tags = sorted(tag_freqs.iteritems(), key=itemgetter(1), reverse=True)[start:end]
        res.body = {'items': tags, 'count': len(tags)}
