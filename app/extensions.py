# -*- coding: utf-8 -*-

"""flask extensions"""

from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

heroku = Heroku()
db = SQLAlchemy()
migrate = Migrate()
