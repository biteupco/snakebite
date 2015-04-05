# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo
from snakebite.constants import TWEET_CHAR_LENGTH


class Menu(mongo.DynamicDocument):
    name = mongo.StringField(required=True)
    price = mongo.DecimalField(min_value=0, required=True)  # defaults to 2 dp, rounded up
    currency = mongo.StringField(required=True, default='JPY')
    rating = mongo.FloatField(min_value=0, max_value=5, default=0)  # current avg rating
    images = mongo.ListField(mongo.URLField())  # list of urls
    tags = mongo.ListField()
    yums = mongo.IntField(min_value=0, default=0)
    restaurant = mongo.ReferenceField('Restaurant', dbref=True)


class Restaurant(mongo.DynamicDocument):
    name = mongo.StringField(required=True)
    address = mongo.StringField(required=True)
    email = mongo.EmailField()
    geolocation = mongo.PointField()
    description = mongo.StringField(max_length=TWEET_CHAR_LENGTH)
    # menus = mongo.ListField(mongo.ReferenceField(Menu, dbref=True))
