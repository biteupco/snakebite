# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from conf import get_config
from snakebite import create_snakebite

# load config via env
env = os.environ.get('BENRI_ENV', 'dev')
config = get_config(env)
snakebite = create_snakebite(**config)
