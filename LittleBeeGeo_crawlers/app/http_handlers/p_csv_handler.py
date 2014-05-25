# -*- coding: utf-8 -*-

from app.constants import *
import random
import math
import base64
import time
import ujson as json
import pandas as pd
import re
from StringIO import StringIO
from datetime import datetime
from pytz import timezone
import urllib

from app import cfg
from app import util

_fill_type_map = {
    u'段': 'section',
    u'巷': 'lane',
    u'弄': 'alley',
    u'號': 'number',
}

_county_and_town_map = {
    u'新北土城': u'新北市土城區',
    u'新北中和': u'新北市中和區',
}

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

    csv_key_list = list(df['csv_key'])

    db_csv_keys = util.db_find('bee', {'csv_key': {'$in': csv_key_list}}, {"_id": False, "csv_key": True})
    db_csv_keys = [db_csv_key.get('csv_key', '') for db_csv_key in db_csv_keys]
    db_csv_keys = [each_key for each_key in db_csv_keys if each_key]
    #is_csv_key_not_in_db = df['csv_key'].isin(db_csv_keys) == False

    df = df[is_csv_key_not_in_db]

    df['address'] = df.apply(lambda x: _parse_address(dict(x), funnel_dict), axis=1)
    df['county_and_town'] = df.apply(lambda x: _parse_county_and_town(dict(x), funnel_dict), axis=1)
    df['google_address'] = df.apply(lambda x: _parse_google_address(dict(x), funnel_dict), axis=1)
    df['deliver_time'] = df.apply(lambda x: _parse_deliver_time(dict(x), funnel_dict), axis=1)
    df['save_time'] = df.apply(lambda x: _parse_save_time(dict(x), funnel_dict), axis=1)
    df['deliver_date'] = df.apply(lambda x: _parse_deliver_date(dict(x), funnel_dict), axis=1)
    df['user_name'] = df.apply(lambda x: _parse_user_name(dict(x), funnel_dict), axis=1)
    df['count'] = df.apply(lambda x: _parse_count(dict(x), funnel_dict), axis=1)
    df['deliver_status'] = df.apply(lambda x: _parse_deliver_status(dict(x), funnel_dict), axis=1)
    df['memo'] = df.apply(lambda x: _parse_memo(dict(x), funnel_dict), axis=1)
    df['version_text'] = df.apply(lambda x: _parse_version_text(dict(x), funnel_dict), axis=1)
    df['versions'] = df.apply(lambda x: _parse_versions(dict(x), funnel_dict), axis=1)

    cfg.logger.debug('df_len: %s', len(df))
    parsed_dict_list = [_parse_dict_row(row, funnel_dict) for (idx, row) in df.iterrows()]

    df = pd.DataFrame(parsed_dict_list)

    df = df[['csv_key', 'deliver_time', 'deliver_date', 'user_name', 'address', 'county_and_town', 'google_address', 'versions', 'version_text', 'count', 'save_time', 'deliver_status', 'memo']]

    results = util.df_to_dict_list(df)

    for each_result in results:
        csv_key = each_result.get('csv_key', '')
        versions = each_result.get('versions', [])
        version_text = each_result.get('version_text', [])
        cfg.logger.debug('to db_update: each_result: %s', each_result)
        util.db_update('bee_csv', {'csv_key': csv_key}, each_result)
        for each_version in versions:
            util.db_update('bee_csv_versions', {'version': each_version}, {csv_key: version_text})

    return (funnel_dict['error_code'], funnel_dict['error_msg'], len(results), results)


def _parse_dict_row(row, funnel_dict):
    dict_row = dict(row)

    return dict_row


def _parse_csv_key(x, funnel_dict):
    x = _unicode_dict(x)
    csv_key = {column: x.get(column, '') for column in [u'時間戳記', u'縣市區']}
    return util.json_dumps(csv_key, sort_keys=True)


def _parse_town(x, funnel_dict):
    x = _unicode_dict(x)

    the_str = x[u'縣市區']
    the_address = x.get(u'路名（區域）', '')

    the_str_match = re.search(ur'^(.*[縣市])(.*[鄉鎮市區])', the_str, flags=re.UNICODE)

    if not the_str_match:
        the_str2 = _purify_county_and_town(the_str, the_address)
        the_str_match = re.search(ur'^(.*[縣市])(.*[鄉鎮市區])', the_str2, flags=re.UNICODE)
        if not the_str_match:
            #cfg.logger.error('unable to parse county and town: the_str: %s the_address: %s', the_str, the_address)
            return ''

    the_str_purify = the_str_match.group(2)

    cfg.logger.debug('the_str: (%s, %s) the_str_purify: (%s: %s)', the_str, the_str.__class__.__name__, the_str_purify, the_str_purify.__class__.__name__)

    return the_str_purify


def _parse_county(x, funnel_dict):
    x = _unicode_dict(x)

    the_str = x[u'縣市區']
    the_address = x.get(u'路名（區域）', '')

    the_str_match = re.search(ur'^(.*[縣市])(.*[鄉鎮市區])', the_str, flags=re.UNICODE)

    if not the_str_match:
        the_str2 = _purify_county_and_town(the_str, the_address)
        the_str_match = re.search(ur'^(.*[縣市])(.*[鄉鎮市區])', the_str2, flags=re.UNICODE)
        if not the_str_match:
            return ''

    the_str_purify = the_str_match.group(1)

    #cfg.logger.debug('the_str: (%s, %s) the_str_purify: (%s: %s)', the_str, the_str.__class__.__name__, the_str_purify, the_str_purify.__class__.__name__)

    return the_str_purify


def _purify_county_and_town(the_str, the_address):
    if _county_and_town_map.get(the_str, ''):
        return _county_and_town_map[the_str]

    return ''


def _parse_user_name(x, funnel_dict):
    x = _unicode_dict(x)
    return x.get(u'暱稱', '')


def _parse_count(x, funnel_dict):
    x = _unicode_dict(x)

    the_str = x[u'數量']
    the_str_match = re.search(ur'^(\d+)', the_str, flags=re.UNICODE)

    if not the_str_match:
        return ''

    the_str_purify = the_str_match.group(1)

    #cfg.logger.debug('the_str: (%s, %s) the_str_purify: (%s: %s)', the_str, the_str.__class__.__name__, the_str_purify, the_str_purify.__class__.__name__)

    return util._int(the_str_purify)


def _parse_deliver_status(x, funnel_dict):
    x = _unicode_dict(x)

    return x.get(u'發送狀況', '')


def _parse_memo(x, funnel_dict):
    x = _unicode_dict(x)

    return x.get(u'備註', '')


def _parse_save_time(x, funnel_dict):
    x = _unicode_dict(x)
    the_str = x.get(u'時間戳記', '')
    #cfg.logger.debug('the_date_time: %s', the_str)

    the_list = the_str.split(' ')
    the_date = the_list[0]
    the_time = the_list[2]
    am_pm = the_list[1]

    the_time_list = the_time.split(':')
    the_hr = util._int(the_time_list[0])

    if the_hr == 12 and am_pm == u'上午': 
        the_time_list[0] = '0'
        the_time = ':'.join(the_time_list)

    if am_pm == u'下午' and the_hr != 12:
        the_time_list[0] = str(util._int(the_time[0]) + 12)
        the_time = ':'.join(the_time_list)

    cfg.logger.debug('the_date: %s the_time: %s', the_date, the_time)

    the_datetime_str = the_date + ' ' + the_time

    the_datetime = datetime.strptime(the_datetime_str, '%Y/%m/%d %H:%M:%S')
    the_timestamp = util.datetime_to_timestamp(the_datetime)

    return the_timestamp


def _parse_deliver_time(x, funnel_dict):
    x = _unicode_dict(x)
    the_str = x.get(u'派送時間', '')
    #cfg.logger.debug('the_date_time: %s', the_str)

    (year, month, day) = _determine_date(the_str, funnel_dict, x)
    the_timestamp = _parse_timestamp(year, month, day, funnel_dict, x)
    
    return the_timestamp


def _determine_date(the_str, funnel_dict, x):
    (year, month, day) = _parse_date1(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date2(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date3(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date4(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date5(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date6(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date7(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date8(the_str)
    if year and month and day:
        return (year, month, day)

    (year, month, day) = _parse_date9(the_str)
    if year and month and day:
        return (year, month, day)

    _add_funnel(funnel_dict, x, 'unable to determine_date: the_str: %s' % (the_str))

    return (0, 0, 0)


def _parse_date1(the_str):
    the_str_match = re.search(ur'(\d+)/(\d+)/(\d+)', the_str, flags=re.UNICODE)

    if not the_str_match:
        return (0, 0, 0)

    num1 = the_str_match.group(1)
    num2 = the_str_match.group(2)
    num3 = the_str_match.group(3)

    (year, month, day) = _determine_date1(num1, num2, num3)
    return (year, month, day)


def _determine_date1(num1_str, num2_str, num3_str):
    num1 = util._int(num1_str)
    num2 = util._int(num2_str)
    num3 = util._int(num3_str)

    year = 2014
    month = 0
    day = 0
    if num1 > 100: # yyyy-MM-dd
        month = num2
        day = num3
    elif num1 == 4 or num1 == 5: # MM-dd-yyyy
        month = num1
        day = num2
    else: # dd-MM-yyyy
        month = num2
        day = num1

    #cfg.logger.debug('num1_str: %s num2_str: %s num3_str: %s num1: %s num2: %s num3: %s year: %s month: %s day: %s', num1_str, num2_str, num3_str, num1, num2, num3, year, month, day)

    if day == 78:
        day = 8

    return (year, month, day)


def _parse_date2(the_str):
    the_str_match = re.search(ur'(\d+)/(\d+)', the_str, flags=re.UNICODE) # MM-dd
    if the_str_match:
        num1 = the_str_match.group(1)
        num2 = the_str_match.group(2)
        year =  2014
        month = util._int(num1)
        day = util._int(num2)
        if day == 22014:
            day = 20
        return (year, month, day)

    return (0, 0, 0)


def _parse_date3(the_str): 
    new_str = re.sub(ur'[.／\\]', '/', the_str, flags=re.UNICODE)
    #cfg.logger.debug('the_str: %s new_str: %s', the_str, new_str)

    return _parse_date1(new_str)


def _parse_date4(the_str): 
    new_str = re.sub(ur'[.／\\]', '/', the_str, flags=re.UNICODE)
    #cfg.logger.debug('the_str: %s new_str: %s', the_str, new_str)

    return _parse_date2(new_str)


def _parse_date5(the_str): # all-number
    the_str = re.sub('-.*', '', the_str)
    if len(the_str) != 8:
        return (0, 0, 0)

    year = util._int(the_str[0:4])
    month = util._int(the_str[4:6])
    day = util._int(the_str[6:8])

    return (year, month, day)


def _parse_date6(the_str): # all-number
    the_str = re.sub('-.*', '', the_str)
    #cfg.logger.debug('the_str: %s len(the_str): %s', the_str, len(the_str))
    if len(the_str) != 7:
        return (0, 0, 0)

    if re.search('^10', the_str):
        year = util._int(the_str[0:3]) + 1911
        month = util._int(the_str[3:5])
        day = util._int(the_str[5:7])
        return (year, month, day)

    month = util._int(the_str[0:1])
    day = util._int(the_str[1:3])
    year = util._int(the_str[3:7])

    return (year, month, day)


def _parse_date7(the_str): # all-number
    the_str = re.sub('-.*', '', the_str)
    #cfg.logger.debug('the_str: %s len(the_str): %s', the_str, len(the_str))
    if len(the_str) != 5:
        return (0, 0, 0)

    month = util._int(the_str[0:1])
    day = util._int(the_str[1:3])
    year = util._int(the_str[3:5]) + 2000

    return (year, month, day)


def _parse_date8(the_str): # all-number
    the_str = re.sub('-.*', '', the_str)
    #cfg.logger.debug('the_str: %s len(the_str): %s', the_str, len(the_str))
    if len(the_str) != 6:
        return (0, 0, 0)

    year = util._int(the_str[0:2]) + 2000
    month = util._int(the_str[2:4])
    day = util._int(the_str[4:6])

    return (year, month, day)


def _parse_date9(the_str): # Apr.
    the_str_match = re.search(ur'Apr\.(\d+)', the_str, flags=re.UNICODE) # MM-dd
    if the_str_match:
        num1 = the_str_match.group(1)
        year =  2014
        month = 4
        day = util._int(num1)
        return (year, month, day)

    return (0, 0, 0)


def _parse_timestamp(year, month, day, funnel_dict, x):
    if not year or not month or not day:
        return 0

    try:
        the_datetime = datetime(year, month, day, tzinfo=timezone("Asia/Taipei"))
        the_timestamp = util.datetime_to_timestamp(the_datetime)
            
        #cfg.logger.debug('year: %s month: %s day: %s the_timestamp: %s', year, month, day, the_timestamp)
    except Exception as e:
        cfg.logger.error('unable to parse deliver time: year: %s month: %s day: %s e: %s', year, month, day, e)
        _add_funnel(funnel_dict, x, 'parse_deliver_time: year: %s month: %s day: %s e: %s' % (year, month, day, e))
        the_timestamp = 0
    
    return the_timestamp


def _parse_deliver_date(x, funnel_dict):
    deliver_time = x.get(u'deliver_time', 0)
    the_datetime = util.timestamp_to_datetime(deliver_time)

    result = the_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    #cfg.logger.debug('deliver_time: %s deliver_date: %s', deliver_time, result)

    return result


def _parse_address(x, funnel_dict):
    #cfg.logger.debug('x: %s', util.json_dumps(x))
    x = _unicode_dict(x)
    the_address = x.get(u'路名（區域）', '')
    return the_address


def _parse_county_and_town(x, funnel_dict):
    #cfg.logger.debug('x: %s', util.json_dumps(x))
    x = _unicode_dict(x)
    county_and_town = x.get(u'縣市區', '')
    new_county_and_town = _county_and_town_map.get(county_and_town, county_and_town)
    cfg.logger.debug('origin_county_and_town: %s new_county_and_town: %s', county_and_town, new_county_and_town)
    return new_county_and_town


def _parse_google_address(x, funnel_dict):
    x = _unicode_dict(x)
    the_address = x.get(u'路名（區域）', '')
    the_address = _sanitize_address(the_address)

    the_address_list = re.split(ur'[ \\（）(),.→＋>＆。;到~～、，&+-]', the_address, flags=re.UNICODE)

    #cfg.logger.debug('the_address: %s len: %s the_address_list: %s', the_address, len(the_address_list), the_address_list)

    parsed_address_list = []
    for (idx, each_address) in enumerate(the_address_list):
        if not each_address:
            continue

        formalized_address_list = _formalize_address(each_address, idx, the_address_list)
        #cfg.logger.debug('each_address: %s formalized_address_list: %s', each_address, formalized_address_list)
        parsed_address_list += formalized_address_list

    previous_parsed_address = {}
    for each_address in parsed_address_list:
        for idx in ['road', 'section', 'lane', 'alley', 'number']:
            if not each_address.get(idx, ''):
                each_address[idx] = previous_parsed_address.get(idx, '')
            else:
                break
        previous_parsed_address = each_address

    #cfg.logger.debug('parse_geo_result: the_address: %s', the_address)
    #for (idx, each_address) in enumerate(parsed_address_list):
        #cfg.logger.debug('parse_geo_result: idx: %s each_address: (%s, %s, %s, %s, %s, %s, %s)', idx, each_address.get('road', ''), each_address.get('section', ''), each_address.get('lane', ''), each_address.get('alley', ''), each_address.get('number', ''), each_address.get('establishment', ''), each_address.get('other', ''))

    #cfg.logger.debug('parsed_address_list: %s', parsed_address_list)

    the_google_info_with_error_code = [_get_google_info_with_error_code_from_address(parsed_address, x) for parsed_address in parsed_address_list]

    the_google_info = [val[1] for val in the_google_info_with_error_code if val[0] == S_OK]

    return the_google_info


def _get_google_info_with_error_code_from_address(parsed_address, x):
    county_and_town = x.get(u'county_and_town', '')
    the_road = '' if not parsed_address.get('road', '') else parsed_address.get('road', '')
    the_section = '' if not parsed_address.get('section', '') else parsed_address.get('section', '') + u'段'
    the_lane = '' if not parsed_address.get('lane', '') else parsed_address.get('lane', '') + u'巷'
    the_alley = '' if not parsed_address.get('alley', '') else parsed_address.get('alley', '') + u'弄'
    the_number = '' if not parsed_address.get('number', '') else parsed_address.get('number', '') + u'號'
    the_establishment = '' if not parsed_address.get('establishment', '') else parsed_address.get('establishment', '')

    full_address = county_and_town + the_road + the_section + the_lane + the_alley + the_number + the_establishment

    cfg.logger.debug('to get_google_info: full_address: %s', full_address)

    #params = 'language=zh-tw&sensor=false&address=' + urllib.quote(full_address.encode('utf-8'))

    #the_url = 'https://maps.googleapis.com/maps/api/geocode/json?' + params

    #http_result = util.http_multiget([the_url])
    
    #result = util.json_loads(http_result.get(the_url, '{}'))

    #cfg.logger.debug('after get google info: full_address: %s result: %s', full_address, result)

    #if not result:
    #    return (S_ERR, {})

    return (S_OK, full_address)


def _sanitize_address(address):
    address = re.sub(ur'四維二街、三街', u'四維二街、四維三街', address, flags=re.UNICODE)
    address = re.sub(ur'和平東三段', u'和平東路三段', address, flags=re.UNICODE)
    address = re.sub(ur'羅斯福路五到六段', u'羅斯福路五段到羅斯福路六段', address, flags=re.UNICODE)
    address = re.sub(ur'左右/', u'左右~', address, flags=re.UNICODE)
    address = re.sub(ur'路/', u'路~', address, flags=re.UNICODE)
    address = re.sub(ur'街/', u'街~', address, flags=re.UNICODE)
    address = re.sub(ur'段/', u'段~', address, flags=re.UNICODE)
    address = re.sub(ur'巷/', u'巷~', address, flags=re.UNICODE)
    address = re.sub(ur'弄/', u'弄~', address, flags=re.UNICODE)
    address = re.sub(ur'號/', u'號~', address, flags=re.UNICODE)
    address = re.sub(ur'段/', u'段~', address, flags=re.UNICODE)
    address = re.sub(ur'路/', u'路~', address, flags=re.UNICODE)
    address = re.sub(ur'文盛里汀洲路三段到羅斯福路24巷', u'文盛里汀洲路三段到文盛里羅斯福路24巷', address, flags=re.UNICODE)
    address = re.sub(ur'(11~15奇數、17~38)', u'', address, flags=re.UNICODE)
    address = re.sub(ur'十字路口', u'', address, flags=re.UNICODE)
    address = re.sub(ur'(義式手工冰淇淋店)', u'', address, flags=re.UNICODE)
    address = re.sub(ur'機車店', u'', address, flags=re.UNICODE)
    address = re.sub(ur'內及周邊', u'', address, flags=re.UNICODE)
    address = re.sub(ur'台灣圖書館門口有發給路人一些', u'國立台灣圖書館', address, flags=re.UNICODE)
    address = re.sub(ur'旁的住宅信箱', u'', address, flags=re.UNICODE)
    address = re.sub(ur'長庚科大班級信箱', u'長庚科技大學', address, flags=re.UNICODE)
    address = re.sub(ur'新世紀誠品文宣櫃和明儀倉庫書局文宣櫃', u'新世紀誠品、明儀倉庫書局', address, flags=re.UNICODE)

    return address


def _formalize_address(address, idx, the_address_list):
    #cfg.logger.debug('to re: address: %s', address)

    address = _sanitize_road(address)

    (the_road, the_section, the_lane, the_alley, the_number, the_other) = _formalize_first_address(address)

    the_road = _sanitize_road(the_road)

    if not the_road and not the_section and not the_lane and not the_alley and not the_number and not the_other:
        return [{'establishment': address}]

    if the_section and re.search(ur'[路]', the_section, flags=re.UNICODE):
        the_other = the_section + u'段'
        the_section = None

    if the_lane and re.search(ur'[路]', the_lane, flags=re.UNICODE):
        the_other = the_lane + u'巷'
        the_lane = None

    if the_alley and re.search(ur'[路]', the_alley, flags=re.UNICODE):
        the_other = the_alley + u'弄'
        the_alley = None

    if the_number and re.search(ur'[路]', the_number, flags=re.UNICODE):
        the_other = the_number + u'號'
        the_numebr = None

    result = {'road': the_road, 'section': the_section, 'lane': the_lane, 'alley': the_alley, 'number': the_number}

    other_address_list = []
    if the_other:
        if re.search(ur'[路街至]', the_other, flags=re.UNICODE):
            other_address_list = _formalize_address(the_other, idx, the_address_list)
        elif re.search(ur'^\d+', the_other, flags=re.UNICODE):
            (fill_type, fill_number) = _formalize_other(the_other, idx, the_address_list)
            _fill_other_to_result(fill_type, fill_number, result)
        else:
            result['other'] = the_other

    #cfg.logger.debug('address: %s result: %s', address, result)

    result_list = [result] + other_address_list

    return result_list


def _formalize_first_address(address):
    (the_number, the_other) = _formalize_first_number(address)
    if the_number:
        return (None, None, None, None, the_number, the_other)

    (the_alley, the_other) = _formalize_first_alley(address)
    if the_alley:
        return (None, None, None, the_alley, None, the_other)

    (the_lane, the_other) = _formalize_first_lane(address)
    if the_lane:
        return (None, None, the_lane, None, None, the_other)

    if re.search(ur'^\d+$', address):
        return (None, None, None, None, None, address)

    the_str_match = re.search(ur'((.*?)[路街])((.*?)段)?((.*?)巷)?((.*?)弄)?((.*?)號)?(.*?)$', address, flags=re.UNICODE)
    if not the_str_match:
        cfg.logger.error('unable to re.search: address: %s', address)
        return (None, None, None, None, None, None)

    the_road2 = the_str_match.group(1)
    the_road = the_str_match.group(2)
    the_section2 = the_str_match.group(3)
    the_section = the_str_match.group(4)
    the_lane2 = the_str_match.group(5)
    the_lane = the_str_match.group(6)
    the_alley2 = the_str_match.group(7)
    the_alley = the_str_match.group(8)
    the_number2 = the_str_match.group(9)
    the_number = the_str_match.group(10)
    the_other = the_str_match.group(11)

    #cfg.logger.debug('address: %s the_road: %s the_section: %s the_lane: %s the_alley: %s the_number: %s the_section2: %s, the_lane2: %s the_alley2: %s the_number2: %s the_other: %s', address, the_road, the_section, the_lane, the_alley, the_number, the_section2, the_lane2, the_alley2, the_number2, the_other)

    return (the_road2, the_section, the_lane, the_alley, the_number, the_other)


def _formalize_first_number(address):
    the_str_match = re.search(ur'^(\d+)號(.*?)$', address, flags=re.UNICODE)
    if not the_str_match:
        return (None, address)

    the_number = the_str_match.group(1)
    the_other = the_str_match.group(2)

    return (the_number, the_other)


def _formalize_first_alley(address):
    the_str_match = re.search(ur'^(\d+)弄(.*?)$', address, flags=re.UNICODE)
    if not the_str_match:
        return (None, address)

    the_alley = the_str_match.group(1)
    the_other = the_str_match.group(2)

    return (the_alley, the_other)


def _formalize_first_lane(address):
    the_str_match = re.search(ur'^(\d+)巷(.*?)$', address, flags=re.UNICODE)
    #cfg.logger.debug('address: %s the_str_match: %s', address, the_str_match)
    if not the_str_match:
        return (None, address)

    the_lane = the_str_match.group(1)
    the_other = the_str_match.group(2)

    return (the_lane, the_other)


def _sanitize_road(the_road):
    if not the_road:
        return ''

    for special_roads in [u'和平', u'至善', u'及人']:
        if re.match(special_roads, the_road, flags=re.UNICODE):
            return the_road

    the_road = re.sub(ur'^沿路至', '', the_road)
    the_road = re.sub(ur'^口的', '', the_road)
    the_road = re.sub(ur'^[的跟和至與及]', '', the_road)
    return the_road


def _fill_other_to_result(fill_type, fill_number, result):
    if fill_type == 'none':
        return
    if not result.get(fill_type, ''):
        result[fill_type] = fill_number


def _formalize_other(the_other, idx, the_address_list):
    if idx == len(the_address_list) - 1:
        return ('none', 0)

    the_str_match = re.search(ur'^(\d+)', the_other, flags=re.UNICODE)
    if not the_str_match:
        return ('none', 0)

    fill_number = the_str_match.group(1)

    if not fill_number:
        return ('none', '0')

    the_str_match = re.search(ur'([段巷弄號])', the_other, flags=re.UNICODE)
    if the_str_match:
        fill_type = _formalize_fill_type(the_str_match.group(1))
        return (fill_type, fill_number)

    for each_idx in range(idx + 1, len(the_address_list)):
        each_address = the_address_list[each_idx]
        the_str_match = re.search(ur'([段巷弄號])', each_address, flags=re.UNICODE)
        if the_str_match:
            fill_type = _formalize_fill_type(the_str_match.group(1))
            return (fill_type, fill_number)

    return ('none', '0')


def _formalize_fill_type(the_str):
    return _fill_type_map.get(the_str, '')


def _parse_version_text(x, funnel_dict):
    x = _unicode_dict(x)
    version_text = x.get(u'檔案版本', '')

    return version_text


def _parse_versions(x, funnel_dict):
    x = _unicode_dict(x)
    the_versions = x.get(u'檔案版本', '')
    the_versions = the_versions.strip()

    versions = re.split(ur'[、+]', the_versions, flags=re.UNICODE)

    versions = [version.lower() for version in versions]

    return versions


def _unicode_dict(the_dict):
    return {key.decode('utf-8') if key.__class__.__name__ == 'str' else key: val.decode('utf-8') if val.__class__.__name__ == 'str' else val for (key, val) in the_dict.iteritems()}


def _add_funnel(funnel_dict, x, the_str):
    csv_key = x.get(u'csv_key')
    if csv_key not in funnel_dict:
        funnel_dict[csv_key] = []

    cfg.logger.error('funnel: the_str: %s', the_str)
    funnel_dict[csv_key].append(the_str)
