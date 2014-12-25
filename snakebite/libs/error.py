# -*- coding: utf-8 -*-

import falcon


class HTTPBadRequest(falcon.HTTPBadRequest):
    """
    wrapper for HTTP Bad Request response
    status code: 400
    """
    pass


class HTTPUnauthorized(falcon.HTTPUnauthorized):
    """
    wrapper for HTTP Unauthorized response
    status code: 401
    may no longer be needed when we use talons.auth for authentication
    """
    pass
