# -*- coding: utf-8 -*-

from __future__ import absolute_import

from mongoengine.errors import (DoesNotExist, MultipleObjectsReturned,
                                ValidationError)

from snakebite.models.user import User


def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except (DoesNotExist, MultipleObjectsReturned, ValidationError):
        return None
