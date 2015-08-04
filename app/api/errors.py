# -*- coding: utf-8 -*-

"""api base error handlers"""

from flask import request, jsonify


def api_exception_handler(ex):
    """error handler for ApplicationException"""
    suppress = request.args.get('suppress_response_codes', None)

    if suppress and (suppress.lower() in ['true', '1']):
        return jsonify(ex.to_json())
    else:
        status_code = ex.status_code
        ex.status_code = None
        return jsonify(ex.to_json()), status_code
