# -*- coding: utf-8 -*-

from __future__ import absolute_import

import decimal

import colander

from snakebite.constants import TWEET_CHAR_LENGTH
from snakebite.controllers.schema.common import Geolocation, Images, Tags
from snakebite.helpers.schema import Currency


class MenuSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    price = colander.SchemaNode(colander.Decimal(quant='1.00', rounding=decimal.ROUND_UP))  # 2dp, rounded up
    currency = colander.SchemaNode(Currency(), validator=Currency.is_valid, missing='JPY')
    images = Images()
    tags = Tags()


class MenuCreateSchema(MenuSchema):
    restaurant_id = colander.Schema(colander.String())


class Menus(colander.SequenceSchema):
    menu = MenuSchema()


class RestaurantSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    address = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String(), validator=colander.Email(), missing='')
    description = colander.SchemaNode(colander.String(), missing='', validator=colander.Length(max=TWEET_CHAR_LENGTH))
    geolocation = Geolocation()


class RestaurantCreateSchema(RestaurantSchema):
    menus = Menus()
