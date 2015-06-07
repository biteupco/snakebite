# -*- coding: utf-8 -*-

from __future__ import absolute_import
import __builtin__
import falcon
import logging
import os
from mongoengine import connection
from logging.handlers import TimedRotatingFileHandler
from snakebite.controllers import restaurant, menu, tag, status, rating, user, batch
from snakebite.middlewares.auth import JWTAuthMiddleware
from snakebite.constants import DATETIME_FORMAT, AUTH_SHARED_SECRET_ENV


def create_snakebite(**config):
    snakebite = SnakeBite(config)
    return snakebite


class SnakeBite(object):

    def __init__(self, config):

        self.config = config

        shared_secret = os.getenv(AUTH_SHARED_SECRET_ENV)

        self.app = falcon.API(
            before=[self.cors_middleware()],
            middleware=[JWTAuthMiddleware(shared_secret)]
        )
        self._set_logging()
        self._setup_db()
        self._load_routes()

    def _load_routes(self):
        self.app.add_route('/restaurants', restaurant.Collection())
        self.app.add_route('/restaurants/{id}', restaurant.Item())
        self.app.add_route('/menus', menu.Collection())
        self.app.add_route('/menus/{id}', menu.Item())
        self.app.add_route('/users', user.Collection())
        self.app.add_route('/users/{id}', user.Item())

        # pseudo resources
        self.app.add_route('/ratings/menus/', rating.Collection())
        self.app.add_route('/ratings/menus/{id}', rating.Item())
        self.app.add_route('/tags', tag.Collection())
        self.app.add_route('/status', status.Status())

        # batch resources
        self.app.add_route('/batch/restaurants', batch.RestaurantCollection())

    def cors_middleware(self):
        """
        :return: a middleware function to deal with Cross Origin Resource Sharing (CORS)
        """
        def fn(req, res, params):
            config = self.config['cors']
            allowed_origins = config['allowed_origins'].split(',')
            allowed_headers = config['allowed_headers']
            allowed_methods = config['allowed_methods']

            origin = req.get_header('Origin')
            header = {'Access-Control-Allow-Headers': allowed_headers}
            if origin in allowed_origins:
                header['Access-Control-Allow-Origin'] = origin
            header['Access-Control-Allow-Methods'] = allowed_methods
            header['Allow'] = allowed_methods
            res.set_headers(header)

        return fn

    def _setup_db(self, db_section='mongodb'):

        # get all config values about DB
        db_config = self.config[db_section]  # map

        db_name = db_config.get('name')

        attr_map = {'host': 'str', 'port': 'int', 'username': 'str', 'password': 'str'}

        kwargs = {}
        for key, typ in attr_map.iteritems():
            typecast_fn = getattr(__builtin__, typ)
            # cast the value from db_config accordingly if key-value pair exists
            kwargs[key] = typecast_fn(db_config.get(key)) if db_config.get(key) else None

        connection.disconnect('default')  # disconnect previous default connection if any

        self.db = connection.connect(db_name, **kwargs)

        logging.info('connected to Database: {}'.format(self.db))

    def _set_logging(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, self.config['logging']['level'].upper()))
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     '../logs/snakebite.log')

        # logs will be generated / separated on a daily basis
        fh = TimedRotatingFileHandler(filename=log_file_path, when='D', interval=1)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt=DATETIME_FORMAT
            )
        )
        logger.addHandler(fh)
        return logger
