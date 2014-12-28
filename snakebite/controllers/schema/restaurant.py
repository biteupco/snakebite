# -*- coding: utf-8 -*-

from __future__ import absolute_import
import colander
from snakebite.helpers.schema import CommaList


class CreateRestaurantSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    address = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String(), validator=colander.Email(), missing='')
    description = colander.SchemaNode(colander.String(), missing='')
    tags = colander.SchemaNode(CommaList(), missing='')
