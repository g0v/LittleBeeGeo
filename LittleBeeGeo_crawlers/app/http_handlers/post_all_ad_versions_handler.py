# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def post_all_ad_versions_handler():
    db_results = util.db_find('bee_csv', {"is_processed_ad_version": True, "is_processed_address": True}, {"_id": False, "town": True, "count": True, "deliver_time": True, "deliver_date": True, "save_time": True, "geo": True, "county": True, "address": True, "user_name": True, "is_processed_ad_version": True, "is_processed_address": True, "csv_key": True, "ad_versions": True, "version_text": True, "memo": True, "deliver_status": True})
    for db_result in db_results:
        util.db_update('bee', {'csv_key': csv_key}, db_result)
