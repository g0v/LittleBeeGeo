# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def p_img_info_handler(data):
    cfg.logger.debug('data: %s', data)
    if not data.get('the_id', ''):
        return {"success": False}

    result = util.db_update('bee_img', {'the_id': data.get('the_id', '')}, data, upsert=False)
    if not result:
        return {"success": False}

    return {"success": True}
