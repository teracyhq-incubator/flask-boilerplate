#!/usr/bin/env python

"""command management for the flask app"""

import os

from flask_script import Manager, Shell

from mgr.migrate import MigrateCommand
from app import create_app

app = create_app(os.getenv('APP_CONFIG', 'dev'), os.getenv('APP_INSTANCE_PATH', None))


def make_shell_context():
    from app.extensions import db, mail, auth_datastore
    from app.auth.models import User, Role

    return {'current_app': app, 'db': db, 'mail': mail,
            'auth_datastore': auth_datastore, 'User': User, 'Role': Role}

manager = Manager(app)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
