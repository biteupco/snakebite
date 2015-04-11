# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.tests import get_test_snakebite
from snakebite.controllers import rating
from snakebite.models.restaurant import Restaurant, Menu
from snakebite.models.rating import MenuRating
from snakebite.models.user import User
import json


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
            User(name='Clarke Kent', email='clarke@kent.com', role=1),
            User(name='Bruce Wayne', email='bruce@wayne.com', role=9),
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
        self.resource = rating.Collection()
        self.api = get_test_snakebite().app

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


class TestRatingCollectionPost(TestRatingWithSetup):

    def setUp(self):
        self.resource = rating.Collection()
        self.api = get_test_snakebite().app

        self.api.add_route('/rating/menus', self.resource)
        self.srmock = testing.StartResponseMock()

        self.setup_common_resources_DB()

    def tearDown(self):
        self.tearDownDB()

    def test_on_post(self):
        pass


class TestRatingCollectionDelete(TestRatingWithSetup):

    def setUp(self):
        self.resource = rating.Collection()
        self.api = get_test_snakebite().app

        self.api.add_route('/rating/menus', self.resource)
        self.srmock = testing.StartResponseMock()

        self.setup_common_resources_DB()

    def tearDown(self):
        self.tearDownDB()

    def test_on_delete(self):
        pass


class TestRatingItemGet(TestRatingWithSetup):

    def setUp(self):
        self.resource = rating.Collection()
        self.api = get_test_snakebite().app

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
