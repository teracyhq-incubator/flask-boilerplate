# -*- coding: utf-8 -*-

"""main application entry point"""
import os

from flask import Flask

from .config import BaseConfig, MODES
from .utils import INSTANCE_FOLDER_PATH
from .blueprints import register_blueprints
from .extensions import init_apps

__all__ = ['create_app']


def create_app(config=None, instance_path=None, **kwargs):
    """create Flask app instance"""
    instance_path = instance_path or INSTANCE_FOLDER_PATH
    kwargs['instance_path'] = instance_path

    app = Flask(__name__, **kwargs)
    _configure_app(app, config)
    _configure_hooks(app)
    _configure_blueprints(app)
    _configure_extensions(app)
    _configure_logging(app)
    _configure_template_filters(app)
    _configure_error_handlers(app)
    return app


def _configure_app(app, config=None):
    """configure app with config"""

    if config and type(config) == str and MODES.get(config, None) is not None:
        config = MODES.get(config)

    if config and type(config) == str and os.path.isfile(config):
        app.config.from_pyfile(config)

    elif config and type(config) == str and os.path.isfile(os.path.join(app.instance_path, config)):
        # try to load from instance_folder_path
        app.config.from_pyfile(os.path.join(app.instance_path, config))
    elif config and type(config) == str:
        raise IOError('{}, {}: not found'.format(config, os.path.join(app.instance_path, config)))

    if config and type(config) != str and issubclass(config, BaseConfig):
        app.config.from_object(config)


def _configure_hooks(app):
    """configure hooks"""
    pass


def _configure_blueprints(app):
    """configure blueprints"""
    register_blueprints(app)


def _configure_extensions(app):
    """configure extensions"""
    init_apps(app)


def _configure_logging(app):
    """configure logging"""
    pass


def _configure_template_filters(app):
    """configure template filters"""
    pass


def _configure_error_handlers(app):
    """configure error handlers"""
    pass
