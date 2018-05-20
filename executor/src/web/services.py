# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask import Response
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from service.globals import Globals
from settings.setting import SETTING
from common.const import CONST
from loggers.logger import log


app = Flask(CONST.SYSTEM_FLASK_APP)


@app.route('/' + CONST.SYSTEM_NAME + '/' + CONST.SUBSYSTEM_SCHEDULER + '/v1/alive')
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
