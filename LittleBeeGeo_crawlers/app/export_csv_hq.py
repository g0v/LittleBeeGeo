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

from app import cfg
from app import util

def export_csv_hq(filename, out_filename=None):
    if out_filename is None:
        out_filename = re.sub('\.csv$', '.export.csv', filename)

    df = pd.read_csv(filename)
    
    the_dict_list = util.df_to_dict_list(df)

    for each_dict in the_dict_list:
        road = each_dict.get(u'路名')
        road_list = re.split(ur'[，。]', road)

        for (idx, each_road) in enumerate(road_list):
            cfg.logger.debug('idx: %s each_road: %s', idx, each_road)

        #query_string = each_dict.get(u'縣市區', '')


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
