# -*- coding:utf-8 -*-

from flask import Flask
from gevent.wsgi import WSGIServer

from common.const import CONST
from loggers.logger import log
from resources import init_route
from settings.setting import SETTING

app = Flask(CONST.SYSTEM_FLASK_APP)


def run_web_service():
    log.info('listening {}'.format(SETTING.SERVER_PORT))

    init_route(app)

    http_server = WSGIServer((SETTING.NODE_IP, SETTING.SERVER_PORT), app, backlog=1024)
    http_server.serve_forever()
