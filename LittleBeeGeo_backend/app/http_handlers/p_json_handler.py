# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def p_json_handler(data):
    for each_data in data:
        the_timestamp = util.get_timestamp()
        the_id = str(the_timestamp) + "_" + util.uuid()
        each_data['the_id'] = the_id
        each_data['save_time'] = the_timestamp
        each_data['user_name'] = each_data.get('user_name', '')
        each_data['address'] = each_data.get('address', '')
        each_data['count'] = util._int(each_data['count'])
    util.db_insert('bee', data)

    return {"success": True}
