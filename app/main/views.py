# -*- coding: utf-8 -*-

"""main views"""

from flask import Blueprint


__all__ = ['main']

main = Blueprint('main', __name__)


@main.route('/')
def hello_world():
    """hello world view"""
    return '<h1>Hello World!</h1>'
