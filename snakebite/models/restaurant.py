# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo


class Restaurant(mongo.DynamicDocument):
    name = mongo.StringField(required=True)
    address = mongo.StringField(required=True)
    email = mongo.EmailField(required=True)
    geolocation = mongo.PointField()
    description = mongo.StringField()
    tags = mongo.ListField()
    menus = mongo.SortedListField(mongo.EmbeddedDocumentField(Menu), ordering='rating')

    @property
    def location(self):
        return {
            'address': self.address,
            'geolocation': self.geolocation,
        }


class Menu(mongo.DynamicEmbeddedDocument):
    price = mongo.FloatField(required=True)
    currency = mongo.StringField(required=True, default='JPY')
    rating = mongo.FloatField(min_value=0, max_value=5, default=0)  # current avg rating
    images = mongo.ListField(mongo.URLField())  # list of urls
    tags = mongo.ListField()
