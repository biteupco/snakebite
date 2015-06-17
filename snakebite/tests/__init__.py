# -*- coding: utf-8 -*-
#
# Here lists all convenience / helper methods commonly used for testing purposes

from __future__ import absolute_import
from conf import get_config
from snakebite import create_snakebite
import mock


def get_test_snakebite():
    config = get_config('testing')
    return create_snakebite(**config)


def get_mock_auth_middleware():
    mw = mock.Mock()
    mw.process_request.return_value = None
    return mw
