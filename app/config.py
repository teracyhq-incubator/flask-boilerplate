# -*- coding: utf-8 -*-
"""Different configuration modes"""

import os


class BaseConfig(object):
    """BaseConfig class for other config class to extend"""

    SECRET_KEY = os.getenv('SECRET_KEY', 'base config key')


class DevConfig(BaseConfig):
    """DevConfig for development configuration"""

    DEBUG = True


class TestConfig(BaseConfig):
    """TestConfig for testing configuration"""

    DEBUG = True

    TESTING = True

# for stag or prod config, must not be included on project version controlled

# 2 config modes with string
MODES = {
    'dev': DevConfig,
    'test': TestConfig
}
