# -*- coding: utf-8 -*-

"""main application entry point"""

from flask import Flask


def create_app(config=None, **kwargs):
    """create Flask app instance"""
    app = Flask(__name__, **kwargs)
    _configure_config(app, config)
    _configure_blueprints(app)
    return app


def _configure_config(app, config):
    """configure config"""
    pass


def _configure_blueprints(app):
    """configure blueprints"""
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
