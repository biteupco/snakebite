# -*- coding: utf-8 -*-

from __future__ import absolute_import
import colander


class MenuRatingSchema(colander.MappingSchema):
    menu_id = colander.SchemaNode(colander.String())
    user_id = colander.SchemaNode(colander.String())
    rating = colander.SchemaNode(colander.Float(), validator=colander.Range(min=0.0, max=5.0), missing=1)
