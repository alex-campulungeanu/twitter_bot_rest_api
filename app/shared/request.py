import json
from functools import wraps

from flask import request, abort, Response

def api_response(res, status_code=200):
    """ Custom API Response Function """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

def validate_request(*expected_args):
    """ Validate requests decorator """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_obj = request.get_json()
            for expected_arg in expected_args:
                if json_obj is None or json_obj.get(expected_arg) is None or expected_arg not in json_obj:
                    return api_response({'status':'notok', 'error': f"You must call with all request params: {', '.join(expected_args)}"}, 400)
            return func(*args, **kwargs)
        return wrapper
    return decorator