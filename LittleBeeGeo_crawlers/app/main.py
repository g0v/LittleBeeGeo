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
from app.http_handlers.p_csv_handler import p_csv_handler
from app.http_handlers.get_google_address_handler import get_google_address_handler
from app.http_handlers.get_versions_handler import get_versions_handler

app = Bottle()

@app.post('/post/csv')
def p_csv():
    _log_entry()
    data = _process_body_request()
    return _process_result(p_csv_handler(data, request.content_type))


@app.get('/get/google_address')
def g_google_address():
    _log_entry()
    params = _process_params()
    return _process_result(get_google_address_handler(params))


@app.get('/get/versions')
def g_versions():
    _log_entry()
    params = _process_params()
    return _process_result(get_versions_handler(params))


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


def _process_params():
    return dict(request.params)


def _log_entry(data=''):
    cfg.logger.debug('log_entry_start: url: %s method: %s remote_route: %s request.cotent_type: %s', request.url, request.method, request.remote_route, request.content_type)
    if request.query_string or request.content_length > 0:
        cfg.logger.debug('log_entry_data: url: %s method: %s remote_route: %s query_string: %s content_type: %s content_length: %s content: %s', request.url, request.method, request.remote_route, request.query_string, request.content_type, request.content_length, data)


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
