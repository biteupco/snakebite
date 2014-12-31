# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from ConfigParser import SafeConfigParser


def get_config(env='dev'):
    """
    :return: a dict parsed from a SafeConfigParser object, with config values loaded from file_path
    """
    # default env: 'dev'
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '{}.ini'.format(env))

    config_parser = SafeConfigParser()
    if not config_parser.read(file_path):
        raise IOError('Invalid Config File. ConfigParser could not read config file: {}'.format(file_path))


    config_map = {}
    for section in config_parser.sections():
        config_map[section] = {k: v for (k, v) in config_parser.items(section)}

    return config_map
