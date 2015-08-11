from functools import wraps
import json

from flask import request, Response, current_app, make_response
from flask_classy import FlaskView, get_interesting_members, DecoratorCompatibilityError
import inflection


# TODO(hoatle): support dict return value from the methods

class Resource(FlaskView):
    trailing_slash = False

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

    @classmethod
    def make_proxy_method(cls, name):
        '''Creates a proxy function that can be used by Flasks routing. The
         proxy instantiates the FlaskView subclass and calls the appropriate
         method.

         :param name: the name of the method to create a proxy for
         '''

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, 'before_request'):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = 'before_' + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)
            if not isinstance(response, Response):
                if isinstance(response, tuple):
                    data, code, headers = unpack(response)
                    response = output_json(data, code, headers)
                else:
                    response = output_json(response, 200)

            after_view_name = 'after_' + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, 'after_request'):
                response = i.after_request(name, response)

            return response

        return proxy

    @classmethod
    def register(cls, app, route_base=None, subdomain=None, route_prefix=None,
                 trailing_slash=None):
        if cls is Resource:
            raise TypeError('cls must be a subclass of Resource, not Resource itself')

        if route_base:
            cls.orig_route_base = cls.route_base
            cls.route_base = route_base

        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix

        if not subdomain:
            if hasattr(app, 'subdomain') and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, 'subdomain'):
                subdomain = cls.subdomain

        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash

        members = get_interesting_members(FlaskView, cls)

        special_methods = {
            'get': 'GET',
            'put': 'PUT',
            'patch': 'PATCH',
            'post': 'POST',
            'delete': 'DELETE',
            'index': 'GET',
            'create': 'POST',
            'show': 'GET',
            'update': 'PUT',
            'destroy': 'DELETE'
        }

        for name, value in members:
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
            try:
                if hasattr(value, '_rule_cache') and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)

                        if not subdomain and sub:
                            subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = '%s_%d' % (route_name, idx,)

                        app.add_url_rule(rule, endpoint, proxy, subdomain=subdomain, **options)

                elif special_methods.get(name, None) is not None:

                    methods = [special_methods.get(name).upper()]

                    rule = cls.build_rule('', value)
                    if not cls.trailing_slash:
                        rule = rule.rstrip('/')
                    app.add_url_rule(rule, route_name, proxy, methods=methods, subdomain=subdomain)

                else:
                    route_str = '/%s/' % name
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls.build_rule(route_str, value)
                    app.add_url_rule(rule, route_name, proxy, subdomain=subdomain)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError(
                    'Incompatible decorator detected on %s in class %s' % (name, cls.__name__))

        if hasattr(cls, 'orig_route_base'):
            cls.route_base = cls.orig_route_base
            del cls.orig_route_base

        if hasattr(cls, 'orig_route_prefix'):
            cls.route_prefix = cls.orig_route_prefix
            del cls.orig_route_prefix

        if hasattr(cls, 'orig_trailing_slash'):
            cls.trailing_slash = cls.orig_trailing_slash
            del cls.orig_trailing_slash


def unpack(value):
    '''Return a three tuple of data, code, and headers'''
    if not isinstance(value, tuple):
        return value, 200, {}

    try:
        data, code, headers = value
        return data, code, headers
    except ValueError:
        pass

    try:
        data, code = value
        return data, code, {}
    except ValueError:
        pass

    return value, 200, {}


def output_json(data, code, headers=None):
    '''Makes a Flask response with a JSON encoded body'''

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

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


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
                data, code, headers = unpack(resp)
                return marshal(data, schema, envelope), code, headers
            else:
                return marshal(resp, schema, envelope)

        return decorated

    return wrapper
