# -*- coding: utf-8 -*-

from __future__ import absolute_import
import colander


class Images(colander.SequenceSchema):
    image = colander.SchemaNode(colander.String(), validator=colander.url)
