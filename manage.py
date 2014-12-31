# -*- coding: utf-8 -*-
from __future__ import absolute_import
from snakebite import create_snakebite
from conf import get_config
import os

# load config via env
env = os.environ.get('BENRI_ENV', 'dev')
config = get_config(env)
snakebite = create_snakebite(**config)

