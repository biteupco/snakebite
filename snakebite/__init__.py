# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import mongoengine as mongo
from conf import get_config
from snakebite.controllers import restaurant


class SnakeBite(object):

    __shared_state = {}  # Borg Singleton design pattern

    def __init__(self):
        self.__dict__ = self.__shared_state

        if 'app' not in self.__shared_state:
            self.config = get_config()
            self.app = falcon.API(before=[self.cors_middleware()])

            # load routes
            self.app.add_route('/restaurants', restaurant.Collection())

            # setup database
            self._setup_db()

    def cors_middleware(self):
        """
        :return: a middleware function to deal with Cross Origin Resource Sharing (CORS)
        """
        def fn(req, res, params):
            allowed_origins = self.config.get('cors', 'allowed_origins').split(',')
            allowed_headers = self.config.get('cors', 'allowed_headers').split(',')

            origin = req.get_header('Origin')
            header = {'Access-Control-Allow-Headers': allowed_headers}
            if origin in allowed_origins:
                header['Access-Control-Allow-Origin'] = origin
            res.set_headers(header)

        return fn

    def _setup_db(self, db_section='mongodb'):

        # get all config values about DB
        db_config = dict(self.config.items(db_section))  # map

        db_name = db_config.pop('name')
        db_config['port'] = int(db_config['port'])

        try:
            self.db = mongo.connect(db_name, **db_config)
        except Exception as e:
            raise e

        # log
        # print('connected to Database: {}'.format(self.db))
