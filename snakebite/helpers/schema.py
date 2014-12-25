# -*- coding: utf-8 -*-

import colander


class CommaList(object):
    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return []
        return [item.strip() for item in cstruct.split(',') if item]


class CommaIntList(CommaList):

    def deserialize(self, node, cstruct):
        list = super(CommaIntList, self).deserialize(node, cstruct)
        if not list:
            return []
        return map(int, super(CommaIntList, self).deserialize(node, cstruct))

    @staticmethod
    def is_int_list(node, list):
        error_msg = ('%r is not a valid comma separated list of integers or a single integer.' % list)

        for item in list:
            if not isinstance(item, int):
                raise colander.Invalid(node, error_msg)
