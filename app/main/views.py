# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template
from . import main_bp


@main_bp.route('/')
def hello_world():
    """hello world view"""
    return render_template('main/hello.html')


@main_bp.route('/api/versions')
def api_versions_info():
    return render_template('main/api_versions.json'), 200, {
        'Content-Type': 'application/json; charset=utf-8'
    }
