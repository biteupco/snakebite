# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo


class Role(object):
    # defines all available roles for users
    # this will and should determine the access control permissions for each endpoint
    # TODO: add Restaurant Manager role
    ADMIN = 9
    EMPLOYEE = 8
    USER = 1

    ROLE_MAP = {
        ADMIN: 'admin',
        EMPLOYEE: 'employee',
        USER: 'user'
    }

    @staticmethod
    def get_role_type(role):
        return Role.ROLE_MAP.get(role, 'user')


class User(mongo.DynamicDocument):

    name = mongo.StringField(required=True)
    email = mongo.EmailField(required=True, unique=True)
    role = mongo.IntField(required=True, default=Role.USER)
    facebook_id = mongo.LongField(required=False)  # Facebook ID is numeric but can be pretty big
    twitter_id = mongo.StringField(required=False)  # Twitter ID is alphanumeric

    @property
    def role_type(self):
        return Role.get_role_type(self.role)
