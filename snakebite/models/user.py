# -*- coding: utf-8 -*-

from __future__ import absolute_import
import mongoengine as mongo


class Role(object):
    # defines all available roles for users
    # this will and should determine the access control permissions for each endpoint
    # TODO: add Restaurant Manager role
    ADMIN = 9
    EMPLOYEE = 8
    OWNER = 4
    USER = 1

    ROLE_MAP = {
        ADMIN: 'admin',
        EMPLOYEE: 'employee',
        OWNER: 'restaurant_owner',
        USER: 'user'
    }

    @staticmethod
    def get_role_type(role):
        return Role.ROLE_MAP.get(role, 'user')


class User(mongo.DynamicDocument):

    first_name = mongo.StringField(required=True)
    last_name = mongo.StringField(required=True)
    display_name = mongo.StringField(required=True)
    verification_code = mongo.StringField(required=False)
    email = mongo.EmailField(required=True, unique=True)
    role = mongo.IntField(required=True, default=Role.USER)
    facebook_id = mongo.LongField(required=False)  # Facebook ID is numeric but can be pretty big
    twitter_id = mongo.StringField(required=False)  # Twitter ID is alphanumeric
    address = mongo.StringField(required=False)
    zip_code = mongo.StringField(required=False)
    country_code = mongo.StringField(min_length=2, max_length=2, required=False)  # follows ISO_3166-1
    tel = mongo.StringField(required=False)  # contact number

    @property
    def role_type(self):
        return Role.get_role_type(self.role)

    def role_satisfy(self, role):
        return self.role >= role
