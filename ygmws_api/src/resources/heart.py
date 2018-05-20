from flask import Response
from flask import jsonify
from flask_restful import Resource

from service.globals import Globals


class HeartBeat(Resource):
    def get(self):
        is_normal = Globals.is_normal_status()
        if not is_normal:
            return Response(500)

        return jsonify('yes')
