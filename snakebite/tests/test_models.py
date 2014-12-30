# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.models.restaurant import Restaurant
from snakebite.tests import setup_testDB, teardown_testDB


class TestRestaurant(testing.TestBase):

    @classmethod
    def setUpClass(cls):
        setup_testDB()
        cls.restaurants = [
            {'dict': {'name': 'a', 'description': 'desc A', 'email': 'a@b.com', 'address': 'tokyo', 'tags': []}},
            {'dict': {'name': 'b', 'description': 'desc B', 'email': 'b@a.com', 'address': 'kyoto', 'tags': ['b']}}
        ]

    @classmethod
    def tearDownClass(cls):
        Restaurant.objects.delete()
        teardown_testDB()

    def test_init(self):

        for r in TestRestaurant.restaurants:
            attributes = r['dict']
            restaurant = Restaurant(**attributes)

            for property, value in attributes.iteritems():
                self.assertEquals(getattr(restaurant, property), value)

                # test location property
                expected_location = {
                    'address': getattr(restaurant, 'address'),
                    'geolocation': getattr(restaurant, 'geolocation')
                }

                self.assertDictEqual(restaurant.location, expected_location)

    def test_save(self):

        for i, r in enumerate(TestRestaurant.restaurants):
            attributes = r['dict']
            restaurant = Restaurant(**attributes)
            restaurant.save()
            self.assertEquals(len(Restaurant.objects), i+1)

    def test_remove(self):

        Restaurant.objects(name__in=['a', 'b']).delete()
        self.assertEquals(len(Restaurant.objects), 0)
