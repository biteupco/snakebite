# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

import falcon

from snakebite.controllers.hooks import serialize
from snakebite.libs.error import HTTPServiceUnavailable
from snakebite.models.restaurant import Restaurant

logger = logging.getLogger(__name__)


class Status(object):

    def __init__(self):
        pass

    @falcon.after(serialize)
    def on_get(self, req, res):
        logger.info('status request made')
        try:
            Restaurant.objects.limit(1)
            res.body = {'ok': True}
            logger.info('database query is successful')
        except Exception:
            logger.error('unable to query database successfully.')
            raise HTTPServiceUnavailable("Snakebite server is currently experiencing issues",
                                         "Unable to query database successfully")
