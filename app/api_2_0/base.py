from functools import wraps
import json

from flask import current_app, make_response
from flask_classy import FlaskView
import inflection


# TODO(hoatle): support dict return value from the methods

def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the 'sort_keys' value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', True)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = json.dumps(data, **settings) + '\n'
    headers = headers or {}
    resp = make_response(dumped, code)
    resp.headers['Content-Type'] = 'application/json'
    resp.headers.extend(headers)
    return resp


class Resource(FlaskView):
    trailing_slash = False
    representations = {'application/json': output_json}

    special_methods = {
        'get': ['GET'],
        'put': ['PUT'],
        'patch': ['PATCH'],
        'post': ['POST'],
        'delete': ['DELETE'],
        'index': ['GET'],
        'create': ['POST'],
        'show': ['GET'],
        'update': ['PUT'],
        'destroy': ['DELETE']
    }

    @classmethod
    def get_route_base(cls):
        if cls.route_base is None:
            base_name = None
            if cls.__name__.endswith('API'):
                base_name = cls.__name__[:-3]
            elif cls.__name__.endswith('Resource'):
                base_name = cls.__name__[:-8]

            if base_name is not None:
                return inflection.dasherize(inflection.pluralize(inflection.underscore(base_name)))

        return super(Resource, cls).get_route_base()


    @classmethod
    def build_route_name(cls, method_name):

        if cls.__name__.endswith('API') or cls.__name__.endswith('Resource'):
            if cls.route_base is None:
                return cls.get_route_base() + ':%s' % method_name
            else:
                return cls.route_base + ':%s' % method_name

        return super(Resource, cls).build_route_name(method_name)


def marshal(data, schema=None, envelope=None):
    if schema:
        result = schema.dump(data)  # TODO(hoatle): handle error?
        data = result.data

    if envelope:
        return {envelope: data}
    else:
        return data


def marshal_with(schema=None, envelope=None):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            resp = func(*args, **kwargs)
            if isinstance(resp, tuple):
                data, code, headers = resp
                return marshal(data, schema, envelope), code, headers
            else:
                return marshal(resp, schema, envelope)

        return decorated

    return wrapper
