# -*- coding: utf-8 -*-

from __future__ import absolute_import
from falcon import testing
from snakebite import SnakeBite


class TestMain(testing.TestBase):

    def before(self):
        self.snakebite = SnakeBite()
        self.api = self.snakebite.app

    def test_db(self):
        self.assertIsNone(self.snakebite.db)
