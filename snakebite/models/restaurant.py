# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo


class Restaurant(mongo.Document):
    name = mongo.StringField(required=True)
    address = mongo.StringField(required=True)
    email = mongo.EmailField(required=True)
    geolocation = mongo.PointField()
    description = mongo.StringField()
    tags = mongo.ListField()

    @property
    def location(self):
        return {
            'address': self.address,
            'geolocation': self.geolocation,
        }
