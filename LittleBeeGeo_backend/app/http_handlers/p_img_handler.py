# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
from wand.image import Image
from StringIO import StringIO

from app.constants import *
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

_IMG_TYPES = ['png', 'jpg', 'gif']
_IMG_TYPE_MAP = {
    'jpg': 'jpeg',
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

    (the_thumbnail, thumbnail_postfix) = _make_thumbnail(data, postfix)
    
    the_dir = '/data/thumbnail/bee/' + the_datetime.strftime('%Y-%m-%d')

    util.makedirs(the_dir)

    thumbnail_filename = the_id + '.' + thumbnail_postfix

    with open(the_dir + '/' + thumbnail_filename, 'w') as f:
        f.write(the_thumbnail)

    db_data = {"filename": the_datetime.strftime('%Y-%m-%d/') + filename, "thumbnail_filename": the_datetime.strftime("%Y-%m-%d/") + thumbnail_filename, "the_id": the_id, 'content_type': content_type, 'save_time': the_timestamp}

    util.db_insert('bee_img', [db_data])

    if '_id' in db_data:
        del db_data['_id']

    return db_data


def _parse_postfix(content_type):
    return _CONTENT_TYPE_POSTFIX_MAP.get(content_type.lower(), 'unknown')


def _make_thumbnail(data, postfix):
    if postfix not in _IMG_TYPES:
        postfix = 'png'

    converted_data = ''
    try:
        with Image(blob=data) as img:
            (width, height) = img.size
            (resized_width, resized_height) = _parse_resize(width, height)
            img.resize(resized_width, resized_height)
            converted_data = img.make_blob(_IMG_TYPE_MAP.get(postfix, postfix))
    except Exception as e:
        logging.exception('unable to _make_thumbnail: postfix: %s e: %s', postfix, e)
        converted_data = data

    return (converted_data, postfix)


def _parse_resize(width, height):
    max_size = max(width, height)

    the_ratio = float(RESIZE_SIZE) / max_size
    resize_width = int(width * the_ratio)
    resize_height = int(height * the_ratio)

    cfg.logger.debug('width: %s height: %s resize_width: %s resize_height: %s', width, height, resize_width, resize_height)

    return (resize_width, resize_height)
