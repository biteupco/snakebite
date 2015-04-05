# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo


class Role(object):
    # defines all available roles for users
    # this will and should determine the access control permissions for each endpoint
    ADMIN = 1
    CUSTOMER = 2
    RESTAURANT = 3


class BaseUser(mongo.DynamicDocument):
    meta = {'abstract': True}

    name = mongo.StringField(required=True)
    email = mongo.EmailField(required=True, primary_key=True)


class Customer(BaseUser):
    role = mongo.IntField(required=True, default=Role.CUSTOMER)
    token = mongo.StringField(required=True)  # oauth token, such as from Facebook


class RestaurantManager(BaseUser):
    role = mongo.IntField(required=True, default=Role.RESTAURANT)


class AdminUser(BaseUser):
    role = mongo.IntField(required=True, default=Role.ADMIN)
