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


class HTTPNotAcceptable(falcon.HTTPNotAcceptable):
    """
    wrapper for HTTP Not Acceptable response
    status code: 406
    """
    pass


class HTTPServiceUnavailable(falcon.HTTPServiceUnavailable):
    """
    wrapper for HTTP Service Unavailable response
    status code: 503
    """
    pass
