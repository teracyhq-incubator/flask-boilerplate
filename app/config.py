# -*- coding: utf-8 -*-
"""Different configuration modes"""

import os
from datetime import timedelta


class BaseConfig(object):
    """BaseConfig class for other config class to extend"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'base config key')
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    # SECURITY_CONFIRMABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = SECRET_KEY
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SQLALCHEMY_QUERY_LIMIT = 20

    JWT_AUTH_URL_RULE = None  # disable default JWT auth rule, use flask-restful instead
    JWT_EXPIRATION_DELTA = timedelta(hours=2)
    JWT_ALGORITHMS = ['HS256']
    JWT_MAX_EXPIRATION_DELTA = timedelta(days=60)
    JWT_MIN_EXPIRES_IN = 60 * 5  # 5 mins
    JWT_MAX_EXPIRES_IN = JWT_MAX_EXPIRATION_DELTA.total_seconds()


class DevConfig(BaseConfig):
    """DevConfig for development configuration"""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mysql://root:teracy@localhost:3306/flask_boilerplate')
    # EMAIL SETTINGS, just for real email functioning
    # MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    # MAIL_PORT = os.getenv('MAIL_PORT', 465)
    # MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', True)
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'default gmail email here')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'default gmail password here')


class TestConfig(DevConfig):
    """TestConfig for testing configuration"""

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mysql://root:teracy@localhost:3306/flask_boilerplate_test')
    TESTING = True


# for stag or prod config, must not be included on project version controlled

# 2 config modes with string
MODES = {
    'dev': DevConfig,
    'test': TestConfig
}
