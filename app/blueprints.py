# -*- coding: utf-8 -*-

"""flask blueprints"""

from .main import main_bp
from .api_1_0 import api_bp

__all__ = ['register_blueprints']


def register_blueprints(app):
    """register blueprints"""
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
