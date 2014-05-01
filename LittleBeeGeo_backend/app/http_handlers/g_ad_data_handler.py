# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import pymongo

from app import cfg
from app import util

def g_ad_data_handler():
    db_results_it = util.db_find_it('bee_img', {}, {"_id": False, "name": True, "the_type": True, "the_id": True})
    db_results_it.sort([('the_id', pymongo.DESCENDING)])
    db_results = list(db_results_it)

    return db_results
