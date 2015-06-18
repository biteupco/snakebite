# -*- coding: utf-8 -*-
from __future__ import absolute_import
import jwt
from snakebite.libs.error import HTTPUnauthorized
from snakebite import constants


class JWTAuthMiddleware(object):
    """JWT Authorization Middleware for Snakebite"""

    def __init__(self, secret):
        self._secret = secret

    def _is_user_authorized(self, req, user_id, acl):
        # TODO implement check of acl against user
        return True

    def process_request(self, req, res):

        # get jwt_token from query string
        token = req.get_param('jwt')
        if not token:
            raise HTTPUnauthorized(
                title='Authorization Failed',
                description='No JSON Web Token provided. Unable to authorize user.'
            )

        try:
            decoded = jwt.decode(token, self._secret)
        except jwt.InvalidTokenError:
            raise HTTPUnauthorized(
                title='Authorization Failed',
                description='Invalid JWT token. Unable to decode token.'
            )

        if decoded.pop("iss") != constants.AUTH_SERVER_NAME:
            raise HTTPUnauthorized(
                title='Authorization Failed',
                description='Invalid JWT issuer identity.'
            )

        user_id = decoded.pop("sub")
        acl = decoded.pop("acl")

        # check if user is authorized to this request
        if not self._is_user_authorized(req, user_id, acl):
            raise HTTPUnauthorized(
                title='Authorization Failed',
                description='User does not have privilege/permission to view requested resource.'
            )

        # user is authorized!
        # set user ID in request header
        req.headers[constants.AUTH_HEADER_USER_ID] = user_id
