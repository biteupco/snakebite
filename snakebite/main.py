# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
from snakebite.controllers import restaurant


class SnakeBite(falcon.API):

    def __init___(self):
        # create new SnakeBite app
        super(SnakeBite, self).__init__()

        self.add_route('/restaurants', restaurant.Collection())
        self.db = None
