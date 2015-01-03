# -*- coding: utf-8 -*-

from __future__ import absolute_import
import colander
import decimal
from snakebite.controllers.schema.common import Images, Geolocation
from snakebite.helpers.schema import CommaList, Currency


class MenuSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    price = colander.SchemaNode(colander.Decimal(quant='1.00', rounding=decimal.ROUND_UP))  # 2dp, rounded up
    currency = colander.SchemaNode(Currency(), validator=Currency.is_valid, missing='JPY')
    images = Images()
    tags = colander.SchemaNode(CommaList(), missing='')


class Menus(colander.SequenceSchema):
    menu = MenuSchema()


class RestaurantSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    address = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String(), validator=colander.Email(), missing='')
    description = colander.SchemaNode(colander.String(), missing='')
    geolocation = Geolocation()
    tags = colander.SchemaNode(CommaList(), missing='')
    menus = Menus()
