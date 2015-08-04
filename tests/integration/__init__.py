"""integration tests"""

import unittest
from nose.plugins.attrib import attr
from sqlalchemy_utils import database_exists, create_database

from app import create_app
from app.config import TestConfig
from app.extensions import db

from . import fixtures


@attr('intg')
class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
        db.create_all()
        fixtures.run()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
