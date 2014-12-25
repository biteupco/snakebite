# -*- coding: utf-8 -*-
from __future__ import absolute_import
from snakebite.main import SnakeBite
from snakebite.controllers.restaurant import Restaurant


app = SnakeBite()
app.add_route('/restaurants', Restaurant())
