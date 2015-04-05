# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo
from snakebite.models.user import User
from snakebite.models.restaurant import Menu


class MenuRating(mongo.DynamicDocument):
    # TODO: add compound index on user and menu
    user = mongo.ReferenceField(User, dbref=True)
    menu = mongo.ReferenceField(Menu, dbref=True)
    rating = mongo.FloatField(min_value=0, max_value=5, default=0)  # current avg rating
