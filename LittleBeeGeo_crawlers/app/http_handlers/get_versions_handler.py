# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def get_versions_handler(params):
    n_db_result = util._int(params.get('n', 1))
    db_result = util.db_find_it('bee_csv', {'is_processed_address': True, 'is_processed_ad_version': {'$ne': True}}, {'_id': False, 'csv_key': True, 'address': True, 'google_address': True, 'geo': True, 'version_text': True, 'versions': True})
    db_result = db_result.limit(n_db_result)

    db_result = list(db_result)

    return {"status": "OK", "result": db_result}
