#!/usr/bin/env python

"""command management for the flask app"""

import os

from flask.ext.script import Manager

from app import create_app

app = create_app(os.getenv('APP_CONFIG', 'dev'), os.getenv('APP_INSTANCE_PATH', None))

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
