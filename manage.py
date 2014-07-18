#!/usr/bin/env python

"""command management for the flask app"""

from flask.ext.script import Manager

from app import create_app


manager = Manager(create_app)

manager.add_option("-c", "--config", dest="config", required=False)

if __name__ == "__main__":
    manager.run()
