# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
from snakebite.controllers import restaurant


class SnakeBite(object):

    __shared_state = {}  # Borg Singleton design pattern

    def __init__(self, database=None):
        self.__dict__ = self.__shared_state

        if 'app' not in self.__shared_state:
            self.app = falcon.API()
            self.app.add_route('/restaurants', restaurant.Collection())
            self.db = database
