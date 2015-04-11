# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite.models.restaurant import Restaurant, Menu


class TestMenu(testing.TestBase):

    def setUp(self):
        self.restaurant = Restaurant(**{
            'name': 'a',
            'description': 'desc',
            'email': 'a@b.com',
            'address': 'Asakusa, Taito-ku, Tokyo',
            'geolocation': [139.79843, 35.712074]
        })

        self.menus = [
            {'name': 'menu1', 'price': 200, 'currency': 'JPY', 'rating_total': 0.0, 'rating_count': 0, 'images': [], 'tags': ['chicken'], 'restaurant': self.restaurant},
            {'name': 'menu2', 'price': 450, 'currency': 'JPY', 'rating_total': 7.0, 'rating_count': 2, 'images': [], 'tags': ['curry'], 'restaurant': self.restaurant},
        ]

    def tearDown(self):
        Menu.objects.delete()
        Restaurant.objects.delete()

    def test_init(self):

        for m in self.menus:
            menu = Menu(**m)

            for property, value in m.iteritems():
                self.assertEquals(getattr(menu, property), value)
            self.assertEqual(menu.rating, 0.00 if not menu.rating_count else float(menu.rating_total / menu.rating_count))
