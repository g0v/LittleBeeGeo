# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def g_ad_data_handler():
    db_results = util.db_find('bee_img', {}, {"_id": False, "name": True, "the_type": True, "the_id": True})

    return db_results
