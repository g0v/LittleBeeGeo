# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def post_ad_version_handler(params):
    csv_key = params.get('csv_key', '')
    if not csv_key:
        return {"success": False, "error_msg": "no csv_key"}

    ad_versions = params.get('ad_versions', [])

    cfg.logger.debug('to update ad_versions: csv_key: %s ad_versions: %s', csv_key, ad_versions)

    util.db_update('bee_csv', {'csv_key': csv_key}, {'ad_versions': ad_versions, "is_processed_ad_version": True})

    db_result = util.db_find_one('bee_csv', {"csv_key": csv_key}, {"_id": False, "town": True, "count": True, "deliver_time": True, "deliver_date": True, "save_time": True, "geo": True, "county": True, "address": True, "user_name": True, "is_processed_ad_version": True, "is_processed_address": True, "csv_key": True, "ad_versions": True, "version_text": True, "memo": True, "deliver_status": True})

    the_id = str(db_result.get('save_time', 0)) + "_" + util.uuid()

    db_result['the_id'] = the_id

    if db_result.get('is_processed_ad_version', False) and db_result.get('is_processed_address', False):
        util.db_update('bee', {'csv_key': csv_key}, db_result)
