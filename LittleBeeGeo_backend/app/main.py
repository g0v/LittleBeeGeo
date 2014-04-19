#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.constants import *

import gevent.monkey; gevent.monkey.patch_all()
from bottle import Bottle, request, response, route, run, post, get, static_file, redirect, HTTPError, view, template

import random
import math
import base64
import time
import ujson as json
import sys
import argparse

from app import cfg
from app import util
from app.gevent_server import GeventServer
from app.http_handlers.p_json_handler import p_json_handler
from app.http_handlers.g_json_handler import g_json_handler


app = Bottle()

@app.get('/')
def dummy():
    return _process_result("1")

@app.get('/index.html')
def g_index():
    cfg.logger.debug('/index.html: static/index.html')
    return static_file('static/index.html', root='.')


@app.get('/js/<filepath:path>')
def g_static(filepath):
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/js/' + filepath, root='.')


@app.get('/css/<filepath:path>')
def g_static2(filepath):
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/css/' + filepath, root='.')


@app.get('/font/<filepath:path>')
def g_static3(filepath):
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/font/' + filepath, root='.')


@app.get('/views/<filepath:path>')
def g_static4(filepath):
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/views/' + filepath, root='.')


@app.post('/post/json')
def p_json():
    data = _process_json_request()
    cfg.logger.debug('data: %s', data)
    return _process_result(p_json_handler(data))


@app.get('/get/json')
def g_json():
    return _process_result(g_json_handler())


def _process_json_request():
    f = request.body
    f.seek(0)
    return util.json_loads(f.read())


def _process_result(the_obj):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', '*')
    #cfg.logger.debug('the_obj: %s', the_obj)
    response.content_type = 'application/json'
    return util.json_dumps(the_obj)


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-l', '--log_filename', type=str, default='', required=False, help="log filename")
    parser.add_argument('-p', '--port', type=str, required=True, help="port")
    parser.add_argument('-u', '--username', type=str, required=False, help="username")
    parser.add_argument('--password', type=str, required=False, help="password")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    username = '' if not hasattr(args, 'username') else args.username
    password = '' if not hasattr(args, 'password') else args.password
    cfg.init({"port": args.port, "ini_filename": args.ini, 'username': '', 'password': '', 'log_filename': args.log_filename})

    run(app, host='0.0.0.0', port=cfg.config.get('port'), server=GeventServer)
