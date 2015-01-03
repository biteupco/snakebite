# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.models.restaurant import Restaurant, Menu


class TestRestaurant(testing.TestBase):

    def setUp(self):
        self.restaurants = [
            {
                'dict': {
                    'name': 'a',
                    'description': 'desc A',
                    'email': 'a@b.com',
                    'address': 'tokyo',
                    'tags': [],
                    'menus': [
                        {
                            'name': 'menu A',
                            'price': 800.00,
                            'currency': 'JPY',
                            'rating': 0,
                            'images': [
                                'http://benri.jp/1.jpg',
                                'http://benri.jp/2.jpg'
                            ],
                            'tags': []
                        },
                        {
                            'name': 'menu B',
                            'price': 650.00,
                            'currency': 'JPY',
                            'rating': 4,
                            'images': [
                                'http://benri.jp/3.jpg'
                            ],
                            'tags': []
                        }
                    ]
                }
            },
            {
                'dict': {
                    'name': 'b',
                    'description': 'desc B',
                    'email': 'b@a.com',
                    'address': 'kyoto',
                    'tags': ['b'],
                    'menus': [
                        {
                            'name': 'menu ABC',
                            'price': 1000.00,
                            'currency': 'JPY',
                            'rating': 4,
                            'images': [
                                'http://benri.jp/5.jpg'
                            ],
                            'tags': []
                        }
                    ]
                }
            }
        ]

    def tearDown(self):
        Restaurant.objects.delete()

    def test_init(self):

        for r in self.restaurants:
            attributes = r['dict']
            menu_attrs = attributes.pop('menus')
            restaurant = Restaurant(**attributes)
            restaurant.menus = [Menu(**attrs) for attrs in menu_attrs]

            for property, value in attributes.iteritems():
                self.assertEquals(getattr(restaurant, property), value)

                # test location property
                expected_location = {
                    'address': getattr(restaurant, 'address'),
                    'geolocation': getattr(restaurant, 'geolocation')
                }

                self.assertDictEqual(restaurant.location, expected_location)
                self.assertIsNotNone(restaurant.menus)

    def test_save(self):
        for i, r in enumerate(self.restaurants):
            attributes = r['dict']
            menu_attrs = attributes.pop('menus')
            restaurant = Restaurant(**attributes)
            restaurant.menus = [Menu(**attrs) for attrs in menu_attrs]
            restaurant.save()
            self.assertEquals(len(restaurant.menus), len(menu_attrs))
            self.assertEquals(len(Restaurant.objects), i+1)

    def test_remove(self):
        Restaurant.objects(name__in=['a', 'b']).delete()
        self.assertEquals(len(Restaurant.objects), 0)
