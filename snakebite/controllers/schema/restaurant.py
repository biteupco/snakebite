# -*- coding: utf-8 -*-

from __future__ import absolute_import
import colander
from snakebite.helpers.schema import CommaList


class CreateRestaurantSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    location = colander.SchemaNode(colander.String())
    tags = colander.SchemaNode(CommaList(), missing='')
