# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def get_google_address_handler(params):
    n_db_result = util._int(params.get('n', 1))
    db_result = util.db_find_it('bee_csv', {'is_processed_address': {'$ne': True}}, {'_id': False, 'csv_key': True, 'google_address': True, 'address': True, 'county_and_town': True})

    db_result_total = db_result.count()

    db_result = db_result.limit(n_db_result)

    db_result = list(db_result)

    return {"status": "OK", "total": db_result_total, "result": db_result}
