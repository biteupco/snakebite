# -*- coding: utf-8 -*-

from __future__ import absolute_import

import jwt

from snakebite import constants
from snakebite.libs.error import HTTPUnauthorized
from snakebite.models.user import Role
from snakebite.services.user import get_user

# role-based permission control
ACL_MAP = {
    '/menus': {
        'get': Role.USER,
        'post': Role.OWNER
    },
    '/menus/+': {
        'get': Role.USER,
        'put': Role.OWNER,
        'delete': Role.OWNER
    },
    '/restaurants': {
        'get': Role.USER,
        'post': Role.EMPLOYEE
    },
    '/restaurants/+': {
        'get': Role.USER,
        'put': Role.OWNER,
        'delete': Role.OWNER
    },
    '/users': {
        'get': Role.EMPLOYEE,
        'post': Role.EMPLOYEE,
    },
    '/users/+': {
        'get': Role.USER,
        'put': Role.EMPLOYEE,
        'delete': Role.EMPLOYEE
    },
    '/tags': {
        'get': Role.USER
    },
    '/status': {
        'get': Role.USER
    }
}


class JWTAuthMiddleware(object):
    """JWT Authorization Middleware for Snakebite"""

    def __init__(self, secret):
        self._secret = secret

    def _access_allowed(self, req, user):
        method = req.method.lower() or 'get'
        path = req.path.lower()

        if path not in ACL_MAP:
            # try replacing :id value with `+`
            sub_path, _, id = path.rpartition('/')
            if not sub_path:
                return False  # unable to find a logical path for ACL checking
            path = "{}/+".format(sub_path)
            if path not in ACL_MAP:
                return False

        return user.role_satisfy(ACL_MAP[path].get(method, Role.USER))  # defaults to minimal role if method not found

    def _is_user_authorized(self, req, user_id):
        user = get_user(user_id)
        return user is not None and self._access_allowed(req, user)

    def process_request(self, req, res):

        # get jwt_token from query string
        token = req.get_param('token')
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
                description='Invalid JSON Web Token. Unable to decode token.'
            )

        if decoded.pop("iss") != constants.AUTH_SERVER_NAME:
            raise HTTPUnauthorized(
                title='Authorization Failed',
                description='Invalid issuer identity for JSON Web Token.'
            )

        user_id = decoded.pop("sub")
        decoded.pop("acl")

        # check if user is authorized to this request
        if not self._is_user_authorized(req, user_id):
            raise HTTPUnauthorized(
                title='Authorization Failed',
                description='User does not have privilege/permission to view requested resource.'
            )

        # user is authorized!
        # set user ID in request params
        req.params[constants.AUTH_HEADER_USER_ID] = user_id
