# -*- coding: utf-8 -*-

"""main views"""

from flask import Blueprint, render_template


__all__ = ['module']

module = Blueprint('main', __name__)


@module.route('/')
def hello_world():
    """hello world view"""
    return render_template('main/hello.html')
