# -*- coding: utf-8 -*-

"""main views"""

from . import main


@main.route('/')
def hello_world():
    """hello world view"""
    return '<h1>Hello World!</h1>'
