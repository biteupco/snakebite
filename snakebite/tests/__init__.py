# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo


def setup_testDB():

    mongo.connect('benri_test')


def teardown_testDB():
    db = mongo.connect('benri_test')
    db.drop_database('benri_test')
