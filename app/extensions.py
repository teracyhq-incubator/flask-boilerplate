# -*- coding: utf-8 -*-

"""flask extensions"""

from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

__all__ = ['init_apps', 'heroku', 'db', 'migrate']

heroku = Heroku()
db = SQLAlchemy()
migrate = Migrate()


def init_apps(app):
    if app.config['DEBUG']:
        from flask.ext.debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    heroku.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
