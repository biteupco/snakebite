# -*- coding: utf-8 -*-

from __future__ import absolute_import
from snakebite.helpers.json import map_query
from snakebite.libs.error import HTTPBadRequest, HTTPNotAcceptable
import mongoengine as mongo
from bson import json_util
import colander


def deserialize(req, res, resource, schema=None):
    """
    A BEFORE hook function
    Deserializes data from the request object based on HTTP method
    if a colander Schema is provided, further deserialize data with the schema
    updates req.params with the deserialized data, in either 'body' or 'query' key
    :param req: request object
    :param res: response object
    :param resource: response pbject
    :param schema: colander Schema object
    """

    def _is_json_type(content_type):
        return content_type == 'application/json'

    if req.method.upper() in ['POST', 'PUT', 'PATCH']:

        if not _is_json_type(req.content_type):
            raise HTTPNotAcceptable(description='JSON required. '
                                                'Invalid Content-Type\n{}'.format(req.content_type))

        req.params['body'] = {}

        stream = req.stream.read()
        if not stream:
            return

        json_body = json_util.loads(stream)

        if schema:
            try:
                body = schema.deserialize(json_body)
            except colander.Invalid as e:
                raise HTTPBadRequest(title='Invalid Value',
                                     description='Invalid arguments '
                                                 'in params:\n{}'.format(e.asdict()))

        req.params['body'] = body

    elif req.method.upper() in ['OPTIONS', 'HEAD', 'GET', 'DELETE']:

        req.params['query'] = {}

        if not req.query_string:
            return

        query = map_query(req.query_string, ignores=['token'])

        if schema:
            try:
                query = schema.deserialize(query)
            except colander.Invalid as e:
                raise HTTPBadRequest(title='Invalid Value',
                                     description='Invalid arguments '
                                                 'in params:\n{}'.format(e.asdict()))

        req.params['query'] = query


def serialize(req, res, resource):
    """
    An AFTER hook function
    Serializes the data from dict to json-formatted string
    :param req: request object
    :param res: response object
    :param resource: resource object
    """
    def _to_json(obj):
        # base cases:
        if isinstance(obj, mongo.Document):
            return obj.to_mongo()
        if isinstance(obj, dict):
            return {k: _to_json(v) for k, v in obj.iteritems()}
        if isinstance(obj, mongo.queryset.queryset.QuerySet):
            return [_to_json(item) for item in obj]
        if isinstance(obj, list) and isinstance(obj[0], mongo.Document):
            return [_to_json(item) for item in obj]
        return obj

    res.body = json_util.dumps(_to_json(res.body))
