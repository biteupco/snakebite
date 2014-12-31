# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from conf import get_config
from snakebite.controllers import restaurant
from snakebite.constants import DATETIME_FORMAT


class SnakeBite(object):

    __shared_state = {}  # Borg Singleton design pattern

    def __init__(self, database=None):
        self.__dict__ = self.__shared_state

        if 'app' not in self.__shared_state:
            self.config = get_config()
            self.app = falcon.API(before=[self.cors_middleware()])

            self.set_logging()

            # load routes
            self.app.add_route('/restaurants', restaurant.Collection())

            # setup database
            self.db = database

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

    def set_logging(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, self.config.get('logging', 'level').upper()))
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     '../logs/snakebite.log')

        # logs will be generated / separated on a daily basis
        fh = TimedRotatingFileHandler(filename=log_file_path, when='D', interval=1)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(
            logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=DATETIME_FORMAT)
        )
        logger.addHandler(fh)
        return logger
