# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
import logging
import os
from mongoengine import connection
from logging.handlers import TimedRotatingFileHandler
from snakebite.controllers import restaurant
from snakebite.constants import DATETIME_FORMAT


def create_snakebite(**config):
    snakebite = SnakeBite(config)
    return snakebite


class SnakeBite(object):

    def __init__(self, config):

        self.config = config

        self.app = falcon.API(before=[self.cors_middleware()])
        self._set_logging()

        # setup database
        self._setup_db()

        # load routes
        self.app.add_route('/restaurants', restaurant.Collection())

    def cors_middleware(self):
        """
        :return: a middleware function to deal with Cross Origin Resource Sharing (CORS)
        """
        def fn(req, res, params):
            allowed_origins = self.config['cors']['allowed_origins'].split(',')
            allowed_headers = self.config['cors']['allowed_headers'].split(',')

            origin = req.get_header('Origin')
            header = {'Access-Control-Allow-Headers': allowed_headers}
            if origin in allowed_origins:
                header['Access-Control-Allow-Origin'] = origin
            res.set_headers(header)

        return fn

    def _setup_db(self, db_section='mongodb'):

        # get all config values about DB
        db_config = self.config[db_section]  # map

        db_name = db_config.get('name')
        port = int(db_config.get('port'))
        host = db_config.get('host')
        connection.disconnect('default')  # disconnect previous default connection if any
        self.db = connection.connect(db_name, host=host, port=port)

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
            logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=DATETIME_FORMAT)
        )
        logger.addHandler(fh)
        return logger
