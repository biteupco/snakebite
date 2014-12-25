# -*- coding: utf-8 -*-

from __future__ import absolute_import
from snakebite.libs.error import HTTPBadRequest
from snakebite.controllers.hooks import get_json_data
from snakebite.controllers.schema.restaurant import CreateRestaurantSchema
import colander


def validate_create_restaurant(req, res, params):
    json_body = get_json_data(req)

    try:
        req.params['data'] = CreateRestaurantSchema().deserialize(json_body)

    except colander.Invalid as e:
        raise HTTPBadRequest(title='Invalid Value', description='Invalid arugments in params:\n{}'.format(e.asdict()))
