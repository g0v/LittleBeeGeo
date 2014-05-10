# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import pandas as pd
import re
from StringIO import StringIO

from app import cfg
from app import util

def p_csv_handler(data, content_type):
    if content_type != 'text/csv':
        return {"success": False, "error_msg": "content_type"}

    (error_code, error_msg, n_success, results) = _parse_csv(data)

    is_success = error_code == S_OK
    return {"success": is_success, "error_msg": error_msg, "n_success": n_success, "results": results}


def _parse_csv(data):
    f = StringIO(data)

    df = pd.read_csv(f)

    funnel_dict = {"error_code": S_OK, "error_msg": "", "fail": set()}

    for each_column in df.columns:
        df[each_column].fillna('', inplace=True)

    df['csv_key'] = df.apply(lambda x: _parse_csv_key(dict(x), funnel_dict), axis=1)
    df['county'] = df.apply(lambda x: _parse_county(dict(x), funnel_dict), axis=1)
    df['town'] = df.apply(lambda x: _parse_town(dict(x), funnel_dict), axis=1)
    df['deliver_time'] = df.apply(lambda x: _parse_deliver_time(dict(x), funnel_dict), axis=1)
    df['deliver_date'] = df.apply(lambda x: _parse_deliver_date(dict(x), funnel_dict), axis=1)
    df['user_name'] = df.apply(lambda x: _parse_user_name(dict(x), funnel_dict), axis=1)
    df['address'] = df.apply(lambda x: _parse_address(dict(x), funnel_dict), axis=1)
    df['geo'] = df.apply(lambda x: _parse_geo(dict(x), funnel_dict), axis=1)
    df['ad_versions'] = df.apply(lambda x: _parse_ad_versions(dict(x), funnel_dict), axis=1)
    df['count'] = df.apply(lambda x: _parse_count(dict(x), funnel_dict), axis=1)

    cfg.logger.debug('df_len: %s', len(df))
    parsed_dict_list = [_parse_dict_row(row, funnel_dict) for (idx, row) in df.iterrows()]

    df = pd.DataFrame(parsed_dict_list)

    df = df[['csv_key', 'county', 'town', 'deliver_time', 'deliver_date', 'user_name', 'address', 'geo', 'ad_versions', 'count']]

    results = util.df_to_dict_list(df)

    return (funnel_dict['error_code'], funnel_dict['error_msg'], 0, results)


def _parse_dict_row(row, funnel_dict):
    dict_row = dict(row)

    return dict_row


def _parse_csv_key(x, funnel_dict):
    cfg.logger.debug("x: %s", x)
    return util.json_dumps(x)


def _parse_county(x, funnel_dict):
    cfg.logger.debug('x: %s', x)
    return ''


def _parse_town(x, funnel_dict):
    cfg.logger.debug('x: %s', x)
    return ''


def _parse_deliver_time(x, funnel_dict):
    cfg.logger.debug("x: %s", x)
    return 0


def _parse_deliver_date(x, funnel_dict):
    cfg.logger.debug("x: %s", x)
    return ''


def _parse_geo(x, funnel_dict):
    return []


def _parse_ad_versions(x, funnel_dict):
    return []


def _parse_county(x, funnel_dict):
    return ''


def _parse_address(x, funnel_dict):
    return ''


def _parse_user_name(x, funnel_dict):
    return ''


def _parse_count(x, funnel_dict):
    return 0
