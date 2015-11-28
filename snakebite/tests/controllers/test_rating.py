# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

import mock
from falcon import testing

from snakebite.controllers import rating
from snakebite.models.rating import MenuRating
from snakebite.models.restaurant import Menu, Restaurant
from snakebite.models.user import User
from snakebite.tests import get_mock_auth_middleware, get_test_snakebite


class TestRatingWithSetup(testing.TestBase):

    def setup_common_resources_DB(self):
        self.restaurant = Restaurant(name='a', description='desc', email='a@b.com',
                                     address='Asakusa, Taito-ku, Tokyo', geolocation=[139.79843, 35.712074])
        self.restaurant.save()
        self.menus = [
            Menu(name='menu1', price=200, currency='JPY', rating_total=4, rating_count=1, images=[], tags=['chicken'], restaurant=self.restaurant),
            Menu(name='menu2', price=450, currency='JPY', rating_total=7, rating_count=2, images=[], tags=['beef'], restaurant=self.restaurant),
        ]
        for menu in self.menus:
            menu.save()
        self.users = [
            User(first_name='Clarke', last_name='Kent', display_name='Superman', email='clarke@kent.com', role=1),
            User(first_name='Bruce', last_name='Wayne', display_name='Batman', email='bruce@wayne.com', role=9),
        ]
        for user in self.users:
            user.save()

    def tearDownDB(self):
        Restaurant.objects.delete()
        Menu.objects.delete()
        User.objects.delete()
        MenuRating.objects.delete()


class TestRatingCollectionGet(TestRatingWithSetup):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = rating.Collection()
        self.api.add_route('/rating/menus', self.resource)
        self.srmock = testing.StartResponseMock()

        self.setup_common_resources_DB()

        self.ratings = [
            MenuRating(user=self.users[0], menu=self.menus[0], rating=4.0),
            MenuRating(user=self.users[1], menu=self.menus[1], rating=2.0),
            MenuRating(user=self.users[0], menu=self.menus[1], rating=5.0)
        ]
        for r in self.ratings:
            r.save()

    def tearDown(self):
        self.tearDownDB()

    def test_on_get(self):
        tests = [
            {'query_string': '', 'expected': {"status": 400}},
            {'query_string': 'start=1limit=1', 'expected': {"status": 400}},
            {'query_string': 'user_id={}'.format(self.users[0].id), 'expected': {"status": 200, "count": 2}},
            {'query_string': 'user_id={}'.format(self.users[1].id), 'expected': {"status": 200, "count": 1}}
        ]
        for t in tests:
            res = self.simulate_request('/ratings/menus',
                                        query_string=t['query_string'],
                                        method='GET',
                                        headers={'accept': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if t['expected']['status'] != 200:  # expected erroneous requests
                self.assertNotIn('count', body.keys())
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())
                continue

            self.assertItemsEqual(["count", "items"], body.keys())
            want = t['expected']['count']
            got = body['count']
            self.assertEqual(got, want, "{}| got: {}, want: {}".format(t['query_string'], got, want))


class TestRatingItemGet(TestRatingWithSetup):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = rating.Item()
        self.api.add_route('/ratings/menus/{id}', self.resource)
        self.srmock = testing.StartResponseMock()

        self.setup_common_resources_DB()

        self.ratings = [
            MenuRating(user=self.users[0], menu=self.menus[0], rating=4.0),
            MenuRating(user=self.users[1], menu=self.menus[1], rating=2.0),
            MenuRating(user=self.users[0], menu=self.menus[1], rating=5.0)
        ]
        for r in self.ratings:
            r.save()

    def tearDown(self):
        self.tearDownDB()

    def test_on_get(self):
        tests = [
            {'id': 'randomID', 'expected': {'status': 400}},
            {'id': self.menus[0].id, 'expected': {'status': 200, 'count': 1}},
            {'id': self.menus[1].id, 'expected': {'status': 200, 'count': 2}}
        ]

        for t in tests:
            res = self.simulate_request('/ratings/menus/{}'.format(t['id']),
                                        method='GET',
                                        headers={'accept': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if t['expected']['status'] != 200:  # expected erroneous requests
                self.assertNotIn('count', body.keys())
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())
                continue

            got = body['count']
            want = t['expected']['count']
            self.assertEqual(got, want, "{}| got: {}, want: {}".format(t['id'], got, want))


class TestRatingItemPost(TestRatingWithSetup):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = rating.Item()
        self.api.add_route('/ratings/menus/{id}', self.resource)
        self.srmock = testing.StartResponseMock()

        self.setup_common_resources_DB()

    def tearDown(self):
        self.tearDownDB()

    def test_on_post(self):
        tests = [
            {'id': 'randomMenuID', 'data': json.dumps({'user_id': 'randomString', 'rating': 3.0}), 'expected': {'status': 400}},
            {'id': str(self.menus[0].id), 'data': json.dumps({'user_id': 'randomString', 'rating': 3.0}), 'expected': {'status': 400}},
            {
                'id': str(self.menus[0].id),
                'data': json.dumps({
                    'user_id': str(self.users[0].id),
                    'rating': 4.0
                }),
                'expected': {
                    'status': 200,
                    'body': {
                        'rating': 4.0,
                        'menu': {'$id': {'$oid': str(self.menus[0].id)}, '$ref': 'menu'},
                        'user': {'$id': {'$oid': str(self.users[0].id)}, '$ref': 'user'}
                    }
                }
            }
        ]

        for t in tests:
            res = self.simulate_request('/ratings/menus/{id}'.format(id=t['id']),
                                        body=t['data'],
                                        method='POST',
                                        headers={'Content-Type': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if t['expected']['status'] != 200:
                self.assertNotIn('count', body.keys())
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())
                continue

            self.assertDictContainsSubset(t['expected']['body'], body, 'got: {}, want: {}'.format(body, t['expected']['body']))


# class TestRatingItemDelete(TestRatingWithSetup):
#
#     def setUp(self):
#         self.resource = rating.Item()
#         self.api = get_test_snakebite().app
#
#         self.api.add_route('/ratings/menus/{id}', self.resource)
#         self.srmock = testing.StartResponseMock()
#
#         self.setup_common_resources_DB()
#
#         self.ratings = [
#             MenuRating(user=self.users[0], menu=self.menus[0], rating=4.0),
#             MenuRating(user=self.users[1], menu=self.menus[1], rating=2.0),
#             MenuRating(user=self.users[0], menu=self.menus[1], rating=5.0)
#         ]
#         for r in self.ratings:
#             r.save()
#
#     def tearDown(self):
#         self.tearDownDB()
#
#     def test_on_delete(self):
#         tests = [
#             {'id': 'randomMenuID', 'query_string': 'user_id=random', 'expected': {"status": 400}},
#             {'id': str(self.menus[0].id), 'query_string': 'user_id={}'.format("random"), 'expected': {"status": 400}},
#             {'id': str(self.menus[0].id), 'query_string': 'user_id={}'.format(str(self.users[1].id)), 'expected': {"status": 200}},  # none found but we return 200
#             {'id': str(self.menus[1].id), 'query_string': 'user_id={}'.format(str(self.users[1].id)), 'expected': {"status": 200}}
#         ]
#
#         for t in tests:
#             res = self.simulate_request('/ratings/menus/{}'.format(t['id']),
#                                         query_string=t['query_string'],
#                                         method='DELETE',
#                                         headers={'Content-Type': 'application/json'})
#
#             self.assertTrue(isinstance(res, list))
#             body = json.loads(res[0])
#             self.assertTrue(isinstance(body, dict))
#
#             if t['expected']['status'] != 200:
#                 self.assertTrue(isinstance(body, dict))
#                 self.assertIn('title', body.keys())
#                 self.assertIn('description', body.keys())  # error
#
#             else:
#                 self.assertIsNone(body)
#
#         self.assertItemsEqual([], MenuRating.objects(menu=self.menus[1], user=self.users[1]))  # deleted
#         self.assertNotEqual([], MenuRating.objects(menu=self.menus[0], user=self.users[0]))  # not deleted
#         self.assertNotEqual([], MenuRating.objects(menu=self.menus[1], user=self.users[0]))  # not deleted
