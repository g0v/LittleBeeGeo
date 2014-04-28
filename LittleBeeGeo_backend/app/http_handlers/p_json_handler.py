# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
from datetime import datetime
import calendar

from app import cfg
from app import util

_MUST_HAVE_KEYS = ["deliver_date", "ad_versions", "geo"]

_OPTIONAL_KEYS = ["deliver_time", "count", "user_name", "address", "county", "town", "deliver_status", "memo"]


def p_json_handler(data):
    '''
    data: [{deliver_time, deliver_date, ad_versions, geo, count, user_name, address, county, town, deliver_status, memo}]
    deliver_date: time in iso-8601 format (with millisecond precision)
    deliver_time: deliver_date as timestamp (secs after Unix epoch) in int.
    ad_versions: list of ad_versions. the name of ad is based on "name" in /get/adData
    geo: geojson format. accepting LineString and Point
    count: in int number
    user_name: string
    address: string
    county: string, based on app/scripts/services/TWCounties in frontend
    town: string, based on app/scripts/services/TWTown in frontend
    deliver_status: string
    memo: string

    ex: {"town":"東區","count":10,"deliver_time":1398724259,"deliver_date":"2014-04-28T22:30:59.383Z","geo":[{"type":"LineString","coordinates":[[120.99337719999994,24.7905385],[120.99452376365662,24.79139038370729],[120.99501729011536,24.79084493848351]]}],"ad_versions":["鳥籠監督條例"],"county":"新竹市","deliver_status":"test","address":"nthu","user_name":"test_user_name","memo":"test"}

    ex2: {"town":"內湖區","count":3000,"deliver_time":1398164891,"deliver_date":"2014-04-22T11:08:11.835Z","geo":[{"type":"Point","coordinates":[121.61277294158936,25.06670789727661]}],"ad_versions":["20140421_二類電信RE"],"county":"台北市","address":"康寧路三段","user_name":"test_user_name"}
    '''
    for each_data in data:
        for key in _MUST_HAVE_KEYS:
            if key not in each_data:
                return {"success": False, "errorMsg": "no key: key: %s each_data: %s" % (key, util.json_dumps(each_data))}

        the_timestamp = util.get_timestamp()
        the_id = str(the_timestamp) + "_" + util.uuid()
        each_data['the_id'] = the_id

        if 'deliver_time' not in each_data:
            (error_code, deliver_time) = _parse_deliver_time(each_data)
            if error_code != S_OK:
                return {"success": False, "error_msg": "deliver_date not fit format: deliver_date: %s each_data: %s" % (each_data.get('deliver_date', ''), util.json_dumps(each_data))}
            each_data['deliver_time'] = deliver_time

        each_data['save_time'] = the_timestamp
        each_data['user_name'] = each_data.get('user_name', '')
        each_data['address'] = each_data.get('address', '')
        each_data['count'] = util._int(each_data['count'])
    util.db_insert('bee', data)

    return {"success": True}


def _parse_deliver_time(data):
    the_datetime = None
    try:
        the_datetime = datetime.strptime(data['deliver_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    except Exception as e:
        cfg.logger.exception('unable to strptime: deliver_date: %s e: %s', each_data.get('deliver_date', ''), e)
        return (S_ERR, None)

    return (S_OK, calendar.timegm(the_datetime.utctimetuple()))
