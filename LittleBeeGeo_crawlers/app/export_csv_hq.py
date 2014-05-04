# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import re
import pandas as pd
import argparse
import urllib

from app import cfg
from app import util

def export_csv_hq(filename, out_filename=None):
    if out_filename is None:
        out_filename = re.sub('\.csv$', '.export.csv', filename)

    df = pd.read_csv(filename, encoding='utf-8')

    df.fillna('', inplace=True)

    the_dict_list = util.df_to_dict_list(df)

    for each_dict in the_dict_list:
        for (key, val) in each_dict.iteritems():
            cfg.logger.debug('key: %s val: %s', key, val)

        county_name = each_dict.get(u'縣市區', '')
        road = each_dict.get(u'路名（區域）', '')

        cfg.logger.debug('county_name: %s road: %s', county_name, road)

        road_list = re.split(ur'[~，。]', road, flags=re.UNICODE)
        road_list = [road for road in road_list if road]

        #for each_road in road_list:
        #    cfg.logger.debug('county_name: %s, each_road: %s', county_name, each_road)

        #for each_road in road_list:
        #    (error_code, geo) = _get_geo(county_name, each_road)


def _get_geo(county_name, each_road):
    query_string = county_name.encode('utf-8') + '+' + each_road.encode('utf-8')

    quote_qs = urllib.quote(query_string)

    url = 'http://maps.googleapis.com/maps/api/geocode/json'

    the_url = url + '?sensor=false&address=' + quote_qs

    results = util.http_multiget([the_url])

    cfg.logger.debug('county_name: %s each_road: %s results: %s', county_name, each_road, results)

    result = util.json_loads(results.get(the_url, ''))

    cfg.logger.debug('county_name: %s each_road: %s result: %s', county_name, each_road, result)

    status = result.get('status', '')

    if status != 'OK':
        cfg.logger.error('unable to retrieve geo info now')
        return (S_ERR, [])


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='LittleBeeGeo_crawler')
    parser.add_argument('-c', '--csv_filename', type=str, required=True, help="xml filename")
    parser.add_argument('-i', '--ini_filename', type=str, required=True, help="ini filename")
    parser.add_argument('-o', '--out_filename', type=str, default=None, required=False, help="log filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini_filename})

    export_csv_hq(args.csv_filename, args.out_filename)
