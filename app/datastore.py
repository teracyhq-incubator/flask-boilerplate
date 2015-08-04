# -*- coding: utf-8 -*-
"""
    datastore
    ~~~~~~~~~

    base datastore module

    How to use:

    - with SQLAlchemy:

    datastore = SQLAlchemyDatastore(db)

    - with MongoDB: (TODO(hoatle): add this)

    and use the methods provided from Datastore
"""

from abc import ABCMeta, abstractmethod


class Datastore(object):
    """Abstract Datastore class.

    .. versionadded:: 0.1.0
    """

    __metaclass__ = ABCMeta

    def __init__(self, db):
        self.db = db

    def commit(self):
        pass

    @abstractmethod
    def put(self, model):
        """Creates a new model or updates an existing model.

        .. versionadded:: 0.1.0

        :param model: the model.
        """

    pass

    @abstractmethod
    def delete(self, model):
        """Deletes an existing model from the database.

        .. versionadded:: 0.1.0

        :param model: the model.
        """
        pass


class SQLAlchemyDatastore(Datastore):
    """SQLAlchemyDatastore class.

    .. versionadded:: 0.1.0
    """

    def commit(self):
        self.db.session.commit()

    def put(self, model):
        self.db.session.add(model)
        # self.db.session.flush()  # TODO(hoatle): do we need this, performance impact?
        return model

    def delete(self, model):
        self.db.session.delete(model)


class MongoEngineDatastore(Datastore):
    """MongoEngineDatastore class.

    .. versionadded:: 0.1.0
    """

    def put(self, model):
        """Saves the model to the database. If the model already exists,
        it will be updated, otherwise it will be created.

        .. versionadded:: 0.1.0

        :param model: the model.
        """
        model.save()
        return model

    def delete(self, model):
        """Deletes an existing model from the database.

        .. versionadded:: 0.1.0

        :param model: the model.
        """
        model.delete()
