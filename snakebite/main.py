# -*- coding: utf-8 -*-

from __future__ import absolute_import
import falcon


class SnakeBite(falcon.API):

    def __init___(self):
        # create new SnakeBite app
        super(SnakeBite, self).__init__()
        from snakebite.controllers.restaurant import Restaurant

        self.add_route('/restaurants', Restaurant())
        # self.load_routes()
        self.db = None

    def load_routes(self):
        from snakebite.controllers.restaurant import Restaurant

        self.add_route('/restaurants', Restaurant())

        # controller_paths = os.path.join(path, CONTROLLER_DIR)
        # for _, name, _ in pkgutil.iter_modules([controller_paths]):
        #     module_name = 'snakebite.{0}.{1}'.format(CONTROLLER_DIR, name)
        #     module = __import__(module_name, fromlist=[name])
        #
        #     classes = inspect.getmembers(module, inspect.isclass)
        #     for controller_class in classes:
        #         controller_class[1](self)  # init controller class with app
