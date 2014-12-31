# -*- coding: utf-8 -*-

from urlparse import parse_qs


def map_query(string):

    query_map = parse_qs(string)
    if not query_map:
        return query_map

    for k, v in query_map.iteritems():
        if len(v) == 1:
            query_map[k] = v[0]  # 'unlist' values when they are a list of 1 item

    return query_map
