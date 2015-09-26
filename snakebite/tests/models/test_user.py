# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.models.user import User, Role


class TestUser(testing.TestBase):

    def test_role_type(self):
        tests = [
            {'user': User(name='Clarke Kent', email='a@b.com', role=Role.ADMIN), 'expected': {'role_type': 'admin', 'unsatisfy': None}},
            {'user': User(name='Bruce Wayne', email='bat@man.com', role=Role.EMPLOYEE), 'expected': {'role_type': 'employee', 'unsatisfy': [Role.ADMIN]}},
            {'user': User(name='Soup Nazi', email='a@c.com', role=Role.OWNER), 'expected': {'role_type': 'restaurant_owner', 'unsatisfy': [Role.ADMIN, Role.EMPLOYEE]}},
            {'user': User(name='Lois Lane', email='b@c.com', role=Role.USER), 'expected': {'role_type': 'user', 'unsatisfy': [Role.ADMIN, Role.EMPLOYEE, Role.OWNER]}},
            {'user': User(name='Random Passerby', email='whoami@c.com', role=0), 'expected': {'role_type': 'user', 'unsatisfy': [Role.ADMIN, Role.EMPLOYEE, Role.OWNER]}}
        ]

        for t in tests:
            user = t['user']
            expected_role_type = t['expected']['role_type']
            self.assertEqual(user.role_type, expected_role_type)

            if t['expected']['unsatisfy']:
                for role in t['expected']['unsatisfy']:
                    self.assertFalse(user.role_satisfy(role))
