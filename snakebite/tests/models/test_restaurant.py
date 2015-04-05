# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.models.restaurant import Restaurant


class TestRestaurant(testing.TestBase):

    def setUp(self):
        self.restaurants = [
            {
                'dict': {
                    'name': 'a',
                    'description': 'desc A',
                    'email': 'a@b.com',
                    'address': 'tokyo',
                }
            },
            {
                'dict': {
                    'name': 'b',
                    'description': 'desc B',
                    'email': 'b@a.com',
                    'address': 'kyoto',
                }
            }
        ]

    def tearDown(self):
        Restaurant.objects.delete()

    def test_init(self):

        for r in self.restaurants:
            attributes = r['dict']
            restaurant = Restaurant(**attributes)

            for property, value in attributes.iteritems():
                self.assertEquals(getattr(restaurant, property), value)

    def test_save(self):
        for i, r in enumerate(self.restaurants):
            attributes = r['dict']
            restaurant = Restaurant(**attributes)
            restaurant.save()
            self.assertEquals(len(Restaurant.objects), i+1)

    def test_remove(self):
        Restaurant.objects(name__in=['a', 'b']).delete()
        self.assertEquals(len(Restaurant.objects), 0)


