# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon
from snakebite.controllers.hooks import serialize

# This is an example app built with Falcon framework.
# Real projects are not meant to be this trivial, of course.
# To run this, make sure you have the relevant python packages installed
# Once done, you can cd into the parent directory of this file
# (e.g., 'SOMEWHERE/snakebite/snakebite')
# and run the command $: gunicorn example:api
# point your browser to http://localhost:8000/restaurants
# congrats if you see the json body as below!


class Restaurant(object):

    @falcon.after(serialize)
    def on_get(self, req, res):
        """"
        Handles GET requests for Restaurant
        """

        result_json = {
            "list": [
                {
                    "id": 123456,
                    "name": "Example Restaurant",
                    "email": "example-benri@gmail.com",
                    "menus": 3,
                    "tags": ["casual", "lunch", "fusion", "roppongi"]
                },
                {
                    "id": 456789,
                    "name": "Example Restaurant 2",
                    "email": "example-benri@gmail.com",
                    "menus": 2,
                    "tags": ["japanese", "cheap", "soba", "traditional"]
                }
            ],
            "count": 2
        }

        res.status = falcon.HTTP_200
        res.body = result_json


api = application = falcon.API()
api.add_route('/restaurants', Restaurant())
