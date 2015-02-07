# -*- coding: utf-8 -*-


def reformat_geolocations_map_to_list(dct, geolocation_attr_names):
    """
    takes a map object (dct) and updates the attributes listed in geolocation_attr_names from a map of {'lon', 'lat'}
    and converts these attributes to [lon, lat] list instead.
    """

    if type(geolocation_attr_names) is str:
        geolocation_attr_names = [geolocation_attr_names]

    elif type(geolocation_attr_names) is not list:
        raise Exception('either a string of a list of string is required for attribute names')

    for attr_name in geolocation_attr_names:

        geolocation_attr = dct.get(attr_name)

        if _is_valid_geolocation_map(geolocation_attr):
            # update dct if geolocation_attr is a valid map of {'lon', 'lat'}
            dct[attr_name] = [geolocation_attr.get('lon'), geolocation_attr.get('lat')]  # map to list

    return dct


def reformat_geolocations_point_field_to_map(obj, geolocation_attr_names):
    """
    takes an object and updates the attributes listed in geolocation_attr_names from a PointField-like map
    and converts these attributes to a simpler {'lon', 'lat'} map instead.
    """

    if type(geolocation_attr_names) is str:
        geolocation_attr_names = [geolocation_attr_names]

    elif type(geolocation_attr_names) is not list:
        raise Exception('either a string of a list of string is required for attribute names')

    for attr_name in geolocation_attr_names:

        geolocation_attr = getattr(obj, attr_name)

        if _is_valid_geolocation_point_field(geolocation_attr):
            # update dct if geolocation_attr is a valid list of [lon, lat]
            lon, lat = geolocation_attr['coordinates']
            setattr(obj, attr_name, {'lon': lon, 'lat': lat})  # list to map

    return obj


def _is_valid_geolocation_map(geolocation):
    return type(geolocation) is dict and geolocation.get('lon') and geolocation.get('lat')


def _is_valid_geolocation_point_field(geolocation):
    if type(geolocation) is not dict:
        return False
    if geolocation.get('type') != 'Point' or not geolocation.get('coordinates'):
        return False

    return type(geolocation['coordinates']) is list and len(geolocation['coordinates']) == 2
