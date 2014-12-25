# -*- coding: utf-8 -*-


def map_query(string, delim='&'):

    if not string:
        return {}

    def split_kv(kv_pair):
        items = kv_pair.split('=')[:2]
        return tuple(items)

    kv_pair = map(split_kv, string.split(delim))
    return {k: v for (k, v) in kv_pair}
