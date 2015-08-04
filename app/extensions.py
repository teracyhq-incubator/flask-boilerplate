# -*- coding: utf-8 -*-

"""flask extensions"""

from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt import JWT

from .auth.datastore import SQLAlchemyAuthDatastore


__all__ = ['init_apps', 'heroku', 'db', 'migrate', 'mail', 'auth_datastore']

heroku = Heroku()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
security = Security()
cors = CORS()
jwt = JWT()

# models must be imported before datastore initialization
from .auth.models import User, Role

auth_datastore = SQLAlchemyAuthDatastore(db)


def init_apps(app):
    if app.config['DEBUG'] and not app.config['TESTING']:
        from flask_debugtoolbar import DebugToolbarExtension

        DebugToolbarExtension(app)

    heroku.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role))
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)

    admin = Admin(name='flask-boilerplate')
    # add admin model views

    admin.add_view(ModelView(User, db.session, category='Users'))
    admin.add_view(ModelView(Role, db.session, category='Users'))

    admin.init_app(app)
