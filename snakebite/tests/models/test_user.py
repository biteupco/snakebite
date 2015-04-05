# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.models.user import User, Role


class TestUser(testing.TestBase):

    def test_role_type(self):
        tests = [
            {'user': User(name='Clarke Kent', email='a@b.com', role=Role.ADMIN), 'expected': {'role_type': 'admin'}},
            {'user': User(name='Bruce Wayne', email='bat@man.com', role=Role.EMPLOYEE), 'expected': {'role_type': 'employee'}},
            {'user': User(name='Lois Lane', email='b@c.com', role=Role.USER), 'expected': {'role_type': 'user'}},
            {'user': User(name='Random Passerby', email='whoami@c.com', role=0), 'expected': {'role_type': 'user'}}
        ]

        for t in tests:
            user = t['user']
            expected_role_type = t['expected']['role_type']
            self.assertEqual(user.role_type, expected_role_type)
