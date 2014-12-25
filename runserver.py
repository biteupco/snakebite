# -*- coding: utf-8 -*-
from __future__ import absolute_import
from snakebite.main import SnakeBite
from snakebite.controllers import restaurant


app = SnakeBite()
app.add_route('/restaurants', restaurant.Collection())
