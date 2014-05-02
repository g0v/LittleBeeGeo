#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
from lxml import etree
import pandas as pd
import argparse

from app import cfg
from app import util

_OGC_NAMESPACE = "http://www.opengis.net/kml/2.2"

def export_gmap(filename, out_filename=None):
    if out_filename is None:
        out_filename = re.sub('\.kml$', '.csv', filename)

    with open(filename, 'r') as f:
        doc = etree.parse(f)

    placemarks = doc.xpath("//t:Placemark", namespaces={"t": _OGC_NAMESPACE})

    results = [_parse_placemark(placemark) for placemark in placemarks]

    cfg.logger.debug('results: %s', results)

    #results = _flatten_list(results)

    df = pd.DataFrame(results)

    df.to_csv(out_filename, index=False, encoding="utf-8")

    #the_dict_list = [dict(row) for (idx, row) in df.iterrows()]

    #with open(out_filename, 'w') as f:
    #    f.write(json.dumps(the_dict_list))


def _parse_placemark(placemark):
    name = placemark.find("t:name", namespaces={"t": _OGC_NAMESPACE})
    description = placemark.find("t:description", namespaces={"t": _OGC_NAMESPACE})
    polygons = placemark.findall("t:Polygon", namespaces={"t": _OGC_NAMESPACE})
    polygons = [_parse_polygon(polygon) for polygon in polygons]

    line_strings = placemark.findall("t:LineString", namespaces={"t": _OGC_NAMESPACE})
    line_strings = [_parse_line_string(line_string) for line_string in line_strings]

    points = placemark.findall("t:Point", namespaces={"t": _OGC_NAMESPACE})
    points = [_parse_point(point) for point in points]

    user_name = '' if name is None else name.text
    memo = '' if description is None else description.text

    return {"geo": polygons + line_strings + points, "user_name": user_name, "memo": memo}


def _parse_polygon(polygon):
    outer_boundary = polygon.find("t:outerBoundaryIs", namespaces={"t": _OGC_NAMESPACE})

    linear_ring = outer_boundary.find("t:LinearRing", namespaces={"t": _OGC_NAMESPACE})

    coordinates = linear_ring.find("t:coordinates", namespaces={"t": _OGC_NAMESPACE})

    cfg.logger.debug('to _parse_coordinates: coordinates: %s', coordinates)

    coordinates = _parse_coordinates(coordinates)

    return {"type": "LineString", "coordinates": coordinates}


def _parse_line_string(line_string):
    coordinates = line_string.find("t:coordinates", namespaces={"t": _OGC_NAMESPACE})
    coordinates = _parse_coordinates(coordinates)

    return {"type": "LineString", "coordinates": coordinates}


def _parse_point(point):
    coordinates = point.find("t:coordinates", namespaces={"t": _OGC_NAMESPACE})
    coordinates = _parse_coordinates(coordinates)

    return {"type": "Point", "coordinates": coordinates[0]}


def _parse_coordinates(coordinates):
    coordinates_text = coordinates.text
    coordinate_list = coordinates_text.split(' ')
    coordinate_list = [_parse_coordinate(each_coordinate) for each_coordinate in coordinate_list]

    return coordinate_list


def _parse_coordinate(coordinate):
    the_list = coordinate.split(',')

    return the_list[0:1]


def _flatten_list(the_list):
    results = []
    for each_data in the_list:
        results += each_data
    return each_data


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-x', '--xml_filename', type=str, required=True, help="xml filename")
    parser.add_argument('-i', '--ini_filename', type=str, required=True, help="ini filename")
    parser.add_argument('-o', '--out_filename', type=str, default=None, required=False, help="log filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini_filename})

    export_gmap(args.xml_filename, args.out_filename)
