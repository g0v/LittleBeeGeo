# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

_CONTENT_TYPE_POSTFIX_MAP = {
    'image/jpeg': 'jpg',
    'image/jpg': 'jpg',
    'image/gif': 'gif',
    'image/png': 'png',
    'application/pdf': 'pdf',
    'application/x-pdf': 'pdf',
}

def p_img_handler(data, content_type, idx):
    idx = util._int(idx)
    postfix = _parse_postfix(content_type)
    result = _save_img(data, postfix, content_type)
    result['the_idx'] = idx
    return result


def _save_img(data, postfix, content_type):
    the_timestamp = util.get_timestamp()
    the_datetime = util.timestamp_to_datetime(the_timestamp)
    the_id = str(the_timestamp) + "_" + util.uuid()
    filename = the_id + '.' + postfix

    the_dir = '/data/img/bee/' + the_datetime.strftime('%Y-%m-%d')

    util.makedirs(the_dir)

    with open(the_dir + '/' + filename, 'w') as f:
        f.write(data)

    the_thumbnail = _make_thumbnail(data)
    
    the_dir = '/data/thumbnail/bee/' + the_datetime.strftime('%Y-%m-%d')

    util.makedirs(the_dir)

    with open(the_dir + '/' + filename, 'w') as f:
        f.write(the_thumbnail)

    db_data = {"filename": the_datetime.strftime('%Y-%m-%d/') + filename, "the_id": the_id, 'content_type': content_type}

    util.db_insert('bee_img', [db_data])

    return db_data


def _parse_postfix(content_type):
    return _CONTENT_TYPE_POSTFIX_MAP.get(content_type.lower(), 'unknown')


def _make_thumbnail(data):
    return data
