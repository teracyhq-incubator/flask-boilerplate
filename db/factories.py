from factory import Sequence, LazyAttribute, post_generation
from factory.alchemy import SQLAlchemyModelFactory

from app.iorad.models import Role, User
from app.extensions import db


class RoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role
        sqlalchemy_session = db.session

    name = Sequence(lambda n: 'role%s' % n)
    description = Sequence(lambda n: 'role%s description' % n)


class UserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = db.session

    first_name = 'John'
    last_name = 'Doe'
    email = LazyAttribute(lambda user:
                          '{0}.{1}@example.com'.format(user.first_name, user.last_name).lower())

    @post_generation
    def roles(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for role in extracted:
                self.roles.add(role)
