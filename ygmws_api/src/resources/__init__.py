from flask_restful import Api

from common.const import CONST
from .authorization import MWSAuth
from .heart import HeartBeat

route_list = [
    (MWSAuth, CONST.URL_PREFIX + 'mws_auth'),
    (HeartBeat, CONST.URL_PREFIX + 'alive')
]


def init_route(app):
    api = Api(app)
    for route in route_list:
        api.add_resource(*route)
