# -*- coding: utf-8 -*-

"""flask blueprints"""

from .main import module as main_blueprint

__all__ = ['register_blueprints']


def register_blueprints(app):
    """register blueprints"""
    app.register_blueprint(main_blueprint)
