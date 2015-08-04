"""extends flask_migrate"""

from flask_script import prompt_bool
from flask_migrate import MigrateCommand
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.extensions import db
from db import seeds


@MigrateCommand.command
def setup():
    """Create the database, load the schema and initialize it with the seed data."""
    if database_exists(db.engine.url):
        if prompt_bool('{} exists. Do you want to drop and create an empty one?'.format(
                repr(db.engine.url))):
            drop()
        else:
            return

    create_database(db.engine.url)
    db.create_all()
    seed()


@MigrateCommand.command
def seed():
    """Initial the database data by seeding"""
    seeds.run()


@MigrateCommand.command
def drop():
    """Drop the database."""
    if database_exists(db.engine.url):
        drop_database(db.engine.url)
    else:
        print '{} does not exists'.format(repr(db.engine.url))


@MigrateCommand.command
def reset():
    """Drop the database and set it up again.
    This is equivalent to $ manage.py db drop && manage.py db setup"""
    drop()
    setup()
