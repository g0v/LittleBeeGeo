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
from app.http_handlers.p_img_handler import p_img_handler
from app.http_handlers.p_img_info_handler import p_img_info_handler
from app.http_handlers.g_ad_data_handler import g_ad_data_handler
from app.http_handlers.g_thumbnail_handler import g_thumbnail_handler

app = Bottle()

@app.get('/')
def dummy():
    return _process_result("1")

@app.get('/index.html')
def g_index():
    _log_entry()
    cfg.logger.debug('/index.html: static/index.html')
    return static_file('static/index.html', root='.')


@app.get('/js/<filepath:path>')
def g_static(filepath):
    _log_entry()
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/js/' + filepath, root='.')


@app.get('/css/<filepath:path>')
def g_static2(filepath):
    _log_entry()
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/css/' + filepath, root='.')


@app.get('/font/<filepath:path>')
def g_static3(filepath):
    _log_entry()
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/font/' + filepath, root='.')


@app.get('/views/<filepath:path>')
def g_static4(filepath):
    _log_entry()
    cfg.logger.debug('filepath: %s', filepath)
    return static_file('static/views/' + filepath, root='.')

@app.route('/post/img/<idx>', method=["OPTIONS"])
def p_img2(idx):
    _log_entry()
    return _process_result({"success": True})


@app.post('/post/img/<idx>')
def p_img(idx):
    _log_entry()
    data = _process_body_request()
    return _process_result(p_img_handler(data, request.content_type, idx))


@app.route('/post/img_info', method=["OPTIONS"])
def p_img_info2():
    _log_entry()
    return _process_result({"success": True})


@app.post('/post/img_info')
def p_img_info():
    _log_entry()
    data = _process_json_request()
    _log_entry(data)
    return _process_result(p_img_info_handler(data))


@app.get('/get/thumbnail/<img_id>')
def g_thumbnail(img_id):
    _log_entry()
    (content_type, content) = g_thumbnail_handler(img_id)
    return _process_img_result(content_type, content)


@app.get('/get/adData')
def g_ad_data():
    _log_entry()
    return _process_result(g_ad_data_handler())


@app.route('/post/json', method=["POST", "OPTIONS"])
def p_json():
    data = _process_json_request()
    _log_entry(data)
    cfg.logger.debug('data: %s', data)
    return _process_result(p_json_handler(data))


@app.get('/get/json')
def g_json():
    _log_entry()
    return _process_result(g_json_handler())


def _log_entry(data=''):
    cfg.logger.debug('log_entry_start: url: %s method: %s remote_route: %s', request.url, request.method, request.remote_route, request.content_type, request.content_length)
    if query_string or request.content_length > 0:
        cfg.logger.debug('log_entry_data: url: %s method: %s remote_route: %s query_string: %s content_type: %s content_length: %s content: %s', request.url, request.method, request.remote_route, request.query_string, request.content_type, request.content_length, data)


def _process_json_request():
    return util.json_loads(_process_body_request())


def _process_body_request():
    f = request.body
    f.seek(0)
    return f.read()


def _process_result(the_obj):
    response.set_header('Accept', '*')
    response.set_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', '*')
    #cfg.logger.debug('the_obj: %s', the_obj)
    response.content_type = 'application/json'
    return util.json_dumps(the_obj)


def _process_img_result(content_type, content):
    response.set_header('Accept', '*')
    response.set_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', '*')
    #cfg.logger.debug('the_obj: %s', the_obj)
    response.content_type = content_type
    return content


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
