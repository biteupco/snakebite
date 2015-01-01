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


class Currency(object):

    currency_map = {
        'JPY': u'¥',
        'USD': u'$',
        'GBP': u'£',
        'SGD': u'SGD$'
    }

    def deserialize(self, node, cstruct):
        if not cstruct or cstruct is colander.null:
            return 'JPY'
        return cstruct[:3]  # trim to first 3 characters

    @staticmethod
    def is_valid(node, value):
        currency_list = Currency.currency_map.keys()
        error_msg = '%r is not a supported currency. Current supported currencies are %r' % (value, currency_list)

        if value not in currency_list:
            raise colander.Invalid(node, error_msg)
