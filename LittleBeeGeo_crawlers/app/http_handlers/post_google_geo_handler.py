# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def post_google_geo_handler(params):
    csv_key = params.get('csv_key', '')
    if not csv_key:
        return {"success": False, "error_msg": "no csv_key"}

    params['is_processed_address'] = True
    cfg.logger.debug('params: %s', params)

    util.db_update('bee_csv', {"csv_key": csv_key}, params)
    return {"success": True}
