# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def g_thumbnail_handler(img_id):
    db_result = util.db_find_one('bee_img', {'the_id': img_id}, {'_id': False, 'thumbnail_filename': True, 'content_type': True})

    if not db_result:
        return ('image/gif', util.empty_img())

    the_filename = db_result.get('thumbnail_filename', '')

    full_filename = '/data/thumbnail/bee/' + the_filename

    cfg.logger.debug('full_filename: %s', full_filename)

    with open(full_filename, 'r') as f:
        content = f.read()

    content_type = db_result.get('content_type', 'image/jpg')

    return (content_type, content)
