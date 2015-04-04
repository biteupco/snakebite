# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.tests import get_test_snakebite
from snakebite.controllers import restaurant
from snakebite.models.restaurant import Restaurant
from snakebite.constants import TOKYO_GEOLOCATION
import json


class TestRestaurantCollectionGet(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Collection()
        self.api = get_test_snakebite().app

        self.api.add_route('/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()
        self.restaurants = [
            Restaurant(name='a', description='desc', email='a@b.com',
                       address='Asakusa, Taito-ku, Tokyo', geolocation=[139.79843, 35.712074]),
            Restaurant(name='b', description='description', email='b@a.com',
                       address='Roppongi, Minato-ku, Tokyo', geolocation=[139.731443, 35.662836])
        ]
        for r in self.restaurants:
            r.save()

    def tearDown(self):
        Restaurant.objects.delete()

    def test_collection_on_get(self):

        tests = [
            {'query_string': '', 'expected': {"status": 200, "count": 2}},
            {'query_string': 'description=desc', 'expected': {"status": 200, "count": 2}},
            {'query_string': 'description=desc&limit=1', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'description=desc&start=1&limit=2', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'description=description', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'name=c', 'expected': {"status": 200, "count": 0}},
            {'query_string': 'email=b@a.com', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'geolocation=139.731443,35.662836', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'geolocation=ab,cd', 'expected': {"status": 400}},
            {'query_string': 'limit=1', 'expected': {"status": 200, "count": 1}},
            {'query_string': 'start=2&limit=1', 'expected': {"status": 200, "count": 0}},
            {'query_string': 'start=1limit=1', 'expected': {"status": 400}}
        ]
        for t in tests:
            res = self.simulate_request('/restaurants',
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

            self.assertListEqual(["count", "items"], sorted(body.keys()))
            self.assertEqual(body['count'], t['expected']['count'], "{}".format(t['query_string']))


class TestRestaurantCollectionPost(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Collection()
        self.api = get_test_snakebite().app
        self.api.add_route('/restaurants', self.resource)
        self.srmock = testing.StartResponseMock()

    def get_mock_restaurant(self, **kwargs):
        base_restaurant = {
            "name": "KFC",
            "address": "ueno",
            "email": "kf@c.com",
            "menus": [],
            "geolocation": TOKYO_GEOLOCATION
        }
        base_restaurant.update(kwargs)
        return base_restaurant

    def get_mock_menu(self, **kwargs):
        base_menu = {
            "name": "some menu",
            "price": 100.00,
            "currency": 'JPY',
            "images": ["http://kfc.com/1.jpg"],
            "tags": []
        }
        base_menu.update(kwargs)
        return base_menu

    def tearDown(self):
        Restaurant.objects.delete()

    def test_collection_on_post(self):

        restaurant1 = self.get_mock_restaurant(name="First Kitchen")  # with no menus (not good!)
        menus1 = [self.get_mock_menu()]
        restaurant1.update({'menus': menus1})
        restaurant2 = self.get_mock_restaurant()
        menus2 = [self.get_mock_menu(name="menu A"), self.get_mock_menu(name="menu B")]
        restaurant2.update({'menus': menus2})

        tests = [
            {
                'data': json.dumps(restaurant1),
                'expected': {
                    "name": "First Kitchen",
                    "address": "ueno",
                    "description": "",
                    "geolocation": TOKYO_GEOLOCATION,
                    "email": "kf@c.com"
                }
            },
            {
                'data': json.dumps(restaurant2),
                'expected': {
                    "name": "KFC",
                    "address": "ueno",
                    "description": "",
                    "geolocation": TOKYO_GEOLOCATION,
                    "email": "kf@c.com"
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


class TestRestaurantItemGet(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Item()
        self.api = get_test_snakebite().app
        self.api.add_route('/restaurants/{id}', self.resource)
        self.srmock = testing.StartResponseMock()

        restaurants = [
            {
                'name': 'a',
                'description': 'desc A',
                'email': 'a@b.com',
                'address': 'tokyo',
            },
            {
                'name': 'b',
                'description': 'desc B',
                'email': 'b@a.com',
                'address': 'kyoto',
            }
        ]
        self.restaurants = []
        for r in restaurants:
            rest = Restaurant(**r)
            rest.save()
            self.restaurants.append(rest)

    def tearDown(self):
        Restaurant.objects(id__in=[r.id for r in self.restaurants]).delete()

    def test_item_on_get(self):
        tests = [
            {
                'id': r.id,
                'expected': {
                    'status': 200,
                    'id': {
                        '_id': {
                            '$oid': str(r.id)
                        }
                    }
                }
            } for r in self.restaurants
        ]

        for t in tests:
            res = self.simulate_request('/restaurants/{}'.format(t['id']),
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


class TestRestaurantItemDelete(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Item()
        self.api = get_test_snakebite().app
        self.api.add_route('/restaurants/{id}', self.resource)
        self.srmock = testing.StartResponseMock()

        restaurants = [
            {
                'name': 'a',
                'description': 'desc A',
                'email': 'a@b.com',
                'address': 'tokyo',
            },
            {
                'name': 'b',
                'description': 'desc B',
                'email': 'b@a.com',
                'address': 'kyoto',
            }
        ]
        self.restaurants = []
        for r in restaurants:
            rest = Restaurant(**r)
            rest.save()
            self.restaurants.append(rest)

    def tearDown(self):
        Restaurant.objects(id__in=[r.id for r in self.restaurants]).delete()

    def test_item_on_get(self):
        tests = [
            {
                'id': r.id,
                'expected': {
                    'status': 200,
                    'id': {
                        '_id': {
                            '$oid': str(r.id)
                        }
                    }
                }
            } for r in self.restaurants
        ]

        # add next test to delete already deleted restaurant
        tests.append(
            {
                'id': self.restaurants[0].id,
                'expected': {
                    'status': 400
                }
            }
        )

        for t in tests:
            res = self.simulate_request('/restaurants/{}'.format(t['id']),
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


class TestRestaurantItemPut(testing.TestBase):

    def setUp(self):
        self.resource = restaurant.Item()
        self.api = get_test_snakebite().app

        self.api.add_route('/restaurants/{id}', self.resource)
        self.srmock = testing.StartResponseMock()
        self.restaurant = None
        rst = Restaurant(
            name='a',
            description='desc',
            email='a@b.com',
            address='Asakusa, Taito-ku, Tokyo',
            geolocation=[139.79843, 35.712074]
        )

        self.restaurant = rst.save()

    def tearDown(self):
        Restaurant.objects.delete()

    def _get_restaurant_json(self):
        res = self.simulate_request('/restaurants/{}'.format(self.restaurant.id),
                                    method="GET",
                                    headers={'Content-Type': 'application/json'})
        return res[0]

    def test_item_on_put(self):

        original_restaurant_json = self._get_restaurant_json()
        edited_restaurant_json = json.loads(original_restaurant_json)
        edited_restaurant_json.update({'name': 'Test Name'})
        edited_restaurant_json = json.dumps(edited_restaurant_json)

        tests = [
            {
                'id': self.restaurant.id,
                'data': original_restaurant_json,
                'expected': {
                    'status': 200,
                    'body': json.loads(original_restaurant_json)
                }
            },
            {
                'id': self.restaurant.id,
                'data': edited_restaurant_json,
                'expected': {
                    'status': 200,
                    'body': json.loads(edited_restaurant_json)
                }
            },
            {
                'id': "randomID",
                'data': original_restaurant_json,
                'expected': {
                    'status': 400
                }
            }
        ]

        for t in tests:
            res = self.simulate_request('/restaurants/{}'.format(t['id']),
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
