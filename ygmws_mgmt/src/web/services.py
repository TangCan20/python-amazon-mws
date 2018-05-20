# -*- coding:utf-8 -*-

from flask import Flask, jsonify, request
from flask import Response
from flask import render_template
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from common.const import CONST
from loggers.logger import log
from service.globals import Globals
from settings.setting import SETTING
from stats.redis_stats import get_stat, clear_stat

app = Flask(CONST.SYSTEM_FLASK_APP)

__FUNC_MAP__ = {
    'get-stat': get_stat,
    'delete-stat': clear_stat
}


@app.route('/' + CONST.SYSTEM_NAME + '/' + CONST.SUBSYSTEM_MGMT + '/v1/stat',
           methods=[
               CONST.METHOD_GET,
               CONST.METHOD_DELETE])
def api_stat():
    req_args = request.args
    op = req_args.get(CONST.OPERATION)
    key = op + '-' + 'stat'
    log.info('stat api key is {}.'.format(key))
    stat_func = __FUNC_MAP__.get(key)
    if stat_func is None:
        return jsonify('not support'), 400

    result_dict = stat_func()

    log.info('result_dict is {}'.format(result_dict))

    return jsonify(result_dict)


@app.route('/' + CONST.SYSTEM_NAME + '/' + CONST.SUBSYSTEM_MGMT + '/v1/index',
           methods=[
               CONST.METHOD_GET])
def api_index():
    return render_template('index.html')


@app.route('/' + CONST.SYSTEM_NAME + '/' + CONST.SUBSYSTEM_MGMT + '/v1/alive',
           methods=[CONST.METHOD_GET])
def alive():
    is_normal = Globals.is_normal_status()
    if not is_normal:
        return Response(500)

    return jsonify('yes')


def run_web_service():
    log.info('listening {}'.format(SETTING.SERVER_PORT))
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(SETTING.SERVER_PORT)
    IOLoop.instance().start()
