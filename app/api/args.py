# -*- coding: utf-8 -*-

"""support for webargs"""

from webargs import Arg
from functools import wraps
from .utils import extract_filters
from webargs.flaskparser import use_args


def _string_to_boolean(value):
    mappings = {
        'true': True,
        'false': False,
        '1': True,
        '0': False
    }

    return mappings.get(value.lower(), True)

# false or 0 => False; others => True
BoolArg = Arg(bool, use=_string_to_boolean)


def extract_args(arg_map, req=None, locations=None, as_kwargs=False, validate=None):

    def wrapper(func):

        @wraps(func)
        @use_args(arg_map, req=req, locations=locations, as_kwargs=as_kwargs, validate=validate)
        def decorated(resource, req_args, *args, **kwargs):
            filters, req_args = extract_filters(req_args)
            req_args['filters'] = filters

            return func(resource, req_args, *args, **kwargs)

        return decorated
    return wrapper

