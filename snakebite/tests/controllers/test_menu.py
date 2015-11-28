# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

import mock
from falcon import testing

from snakebite.controllers import menu
from snakebite.models.restaurant import Menu, Restaurant
from snakebite.tests import get_mock_auth_middleware, get_test_snakebite


class TestMenuCollectionGet(testing.TestBase):
    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = menu.Collection()
        self.api.add_route('/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()
        self.restaurants = [
            Restaurant(name='a', description='a', email='a@b.com',
                       address='Roppongi Hills, Mori Tower, Minato-ku, Tokyo',
                       geolocation=[139.729183, 35.660429]),  # exactly at Roppongi Hills Mori Tower
            Restaurant(name='z', description='z', email='z@y.com',
                       address='Nishi-Azabu, Minato-ku, Tokyo',
                       geolocation=[139.727553, 35.659599]),  # slightly away from Roppongi
        ]
        for r in self.restaurants:
            r.save()

        self.menus = [
            Menu(name='curry chicken', price=550, currency='JPY', images=[], tags=['chicken', 'curry'], restaurant=self.restaurants[0]),
            Menu(name='keema curry', price=700, currency='JPY', images=[], tags=['indian', 'curry'], restaurant=self.restaurants[0]),
            Menu(name='tempura don', price=600, currency='JPY', images=[], tags=['japanese', 'fried'], restaurant=self.restaurants[1]),
            Menu(name='chahan set', price=900, currency='JPY', images=[], tags=['fried', 'rice'], restaurant=self.restaurants[1]),
            Menu(name='yakisoba', price=400, currency='JPY', images=[], tags=['noodles'], restaurant=self.restaurants[1])
        ]
        for m in self.menus:
            m.save()

    def tearDown(self):
        Restaurant.objects.delete()
        Menu.objects.delete()

    def test_on_get(self):

        tests = [
            {'query_string': 'start=2a', 'expected': {'status': 400}},
            {'query_string': '', 'expected': {'status': 200, 'count': len(self.menus)}},
            {'query_string': 'start=1', 'expected': {'status': 200, 'count': len(self.menus) - 1}},
            {'query_string': 'price=0,500', 'expected': {'status': 200, 'count': 1}},
            {'query_string': 'price=500,0', 'expected': {'status': 200, 'count': 1}},
            {'query_string': 'price=500,800', 'expected': {'status': 200, 'count': 3}},
            {'query_string': 'price=0,800&name=chicken', 'expected': {'status': 200, 'count': 1}},
            {'query_string': 'tags=fried', 'expected': {'status': 200, 'count': 2}},
            {'query_string': 'geolocation=a,35.660429', 'expected': {'status': 400}},
            {'query_string': 'geolocation=139.729183,35.660429', 'expected': {'status': 200, 'count': len(self.menus)}},
            {'query_string': 'geolocation=139.729183,35.660429&maxDistance=100', 'expected': {'status': 200, 'count': 2}},
            {'query_string': 'geolocation=139.729183,35.660429&price=0,600', 'expected': {'status': 200, 'count': 3}},
        ]
        for t in tests:
            res = self.simulate_request('/menus',
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
            got = body['count']
            want = t['expected']['count']
            self.assertEqual(got, want, "{}| got: {}, want: {}".format(t['query_string'], got, want))


class TestMenuCollectionPost(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = menu.Collection()
        self.api.add_route('/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()
        self.restaurant = Restaurant(name='a', description='a', email='a@b.com',
                                     address='Roppongi Hills, Mori Tower, Minato-ku, Tokyo',
                                     geolocation=[139.729183, 35.660429])
        self.restaurant.save()

    def tearDown(self):
        Restaurant.objects(id__in=[self.restaurant.id]).delete()
        Menu.objects().delete()

    def test_on_post(self):
        tests = [
            {
                'data': json.dumps({
                    "name": "menu1",
                    "price": 100.00,
                    "currency": 'JPY',
                    "images": ["http://kfc.com/1.jpg"],
                    "tags": [],
                    "restaurant_id": str(self.restaurant.id)}),
                'expected': {
                    "name": "menu1"
                }
            }
        ]
        for t in tests:
            res = self.simulate_request('/restaurants',
                                        body=t['data'],
                                        method='POST',
                                        headers={'Content-Type': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))
            self.assertDictContainsSubset(t['expected'], body)


class TestMenuItemGet(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = menu.Item()
        self.api.add_route('/menus/{id}', self.resource)
        self.srmock = testing.StartResponseMock()

        self.menus = [
            Menu(name='curry chicken', price=550, currency='JPY', images=[], tags=['chicken', 'curry']),
            Menu(name='keema curry', price=700, currency='JPY', images=[], tags=['indian', 'curry'])
        ]
        for m in self.menus:
            m.save()

    def tearDown(self):
        Menu.objects(id__in=[r.id for r in self.menus]).delete()

    def test_item_on_get(self):
        tests = [
            {
                'id': m.id,
                'expected': {
                    'status': 200,
                    'id': {
                        '_id': {
                            '$oid': str(m.id)
                        }
                    }
                }
            } for m in self.menus
        ]

        for t in tests:
            res = self.simulate_request('/menus/{}'.format(t['id']),
                                        method='GET',
                                        headers={'Content-Type': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if t['expected']['status'] != 200:
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())  # error

            else:
                self.assertDictContainsSubset(t['expected']['id'], body)


class TestMenuItemDelete(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = menu.Item()
        self.api.add_route('/menus/{id}', self.resource)
        self.srmock = testing.StartResponseMock()

        self.menus = [
            Menu(name='curry chicken', price=550, currency='JPY', images=[], tags=['chicken', 'curry']),
            Menu(name='keema curry', price=700, currency='JPY', images=[], tags=['indian', 'curry'])
        ]
        for m in self.menus:
            m.save()

    def tearDown(self):
        Menu.objects(id__in=[m.id for m in self.menus]).delete()

    def test_item_on_get(self):
        tests = [
            {
                'id': m.id,
                'expected': {
                    'status': 200,
                    'id': {
                        '_id': {
                            '$oid': str(m.id)
                        }
                    }
                }
            } for m in self.menus
        ]

        # add next test to delete already deleted menu
        tests.append(
            {
                'id': self.menus[0].id,
                'expected': {
                    'status': 400
                }
            }
        )

        for t in tests:
            res = self.simulate_request('/menus/{}'.format(t['id']),
                                        method='DELETE',
                                        headers={'Content-Type': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])

            if t['expected']['status'] != 200:
                self.assertTrue(isinstance(body, dict))
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())  # error

            else:
                self.assertIsNone(body)


class TestMenuItemPut(testing.TestBase):

    def setUp(self):
        with mock.patch('snakebite.JWTAuthMiddleware', return_value=get_mock_auth_middleware()):
            self.api = get_test_snakebite().app

        self.resource = menu.Item()
        self.api.add_route('/menus/{id}', self.resource)
        self.srmock = testing.StartResponseMock()
        self.menu = None
        mnu = Menu(
            name='menu1',
            price=500,
            currency='JPY',
            tags=['chicken', 'curry'],
            images=[]
        )

        self.menu = mnu.save()

    def tearDown(self):
        Menu.objects.delete()

    def _get_menu_json(self):
        res = self.simulate_request('/menus/{}'.format(self.menu.id),
                                    method="GET",
                                    headers={'Content-Type': 'application/json'})
        return res[0]

    def test_item_on_put(self):

        original_menu_json = self._get_menu_json()
        edited_menu_json = json.loads(original_menu_json)
        edited_menu_json.update({'name': 'Test Menu Name'})
        edited_menu_json = json.dumps(edited_menu_json)

        tests = [
            {
                'id': self.menu.id,
                'data': original_menu_json,
                'expected': {
                    'status': 200,
                    'body': json.loads(original_menu_json)
                }
            },
            {
                'id': self.menu.id,
                'data': edited_menu_json,
                'expected': {
                    'status': 200,
                    'body': json.loads(edited_menu_json)
                }
            },
            {
                'id': "randomID",
                'data': original_menu_json,
                'expected': {
                    'status': 400
                }
            }
        ]

        for t in tests:
            res = self.simulate_request('/menus/{}'.format(t['id']),
                                        body=t['data'],
                                        method='PUT',
                                        headers={'Content-Type': 'application/json'})

            self.assertTrue(isinstance(res, list))
            body = json.loads(res[0])
            self.assertTrue(isinstance(body, dict))

            if t['expected']['status'] != 200:
                self.assertIn('title', body.keys())
                self.assertIn('description', body.keys())  # error

            else:
                self.assertDictEqual(t['expected']['body'], body)
