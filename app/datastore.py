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

from sqlalchemy import desc
import inflection

from .utils import extract_dict, add_filters


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

    def __init__(self, db):
        super(SQLAlchemyDatastore, self).__init__(db)
        self.model_registry = {}
        classes, table_names = [], []
        for clazz in db.Model._decl_class_registry.values():
            try:
                table_names.append(clazz.__tablename__)
                classes.append(clazz)
            except:  # TODO(hoatle): too broad exception
                pass
        for table in db.metadata.tables.items():
            if table[0] in table_names:
                model = classes[table_names.index(table[0])]
                self.model_registry[inflection.underscore(model.__name__)] = model

    def commit(self):
        self.db.session.commit()

    def put(self, model):
        self.db.session.add(model)
        # self.db.session.flush()  # TODO(hoatle): do we need this, performance impact?
        return model

    def delete(self, model):
        self.db.session.delete(model)

    def get_model_class(self, model_name):
        return self.model_registry.get(model_name)

    def get_model_instance(self, model_name, **fields):
        return self.get_model_class(model_name)(**fields)

    # Base CRUD

    def find_by_model_name(self, model_name, q=None, accepted_filter_keys=None, filters=None,
                           sort=None, offset=None, limit=None, **kwargs):

        model_class = self.get_model_class(model_name)
        query = model_class.query.from_self()
        if filters is not None and len(filters) > 0:
            query = add_filters(query, filters, accepted_filter_keys)
        # {key:value,}
        filter_dict = extract_dict(kwargs, extracted_keys=accepted_filter_keys)
        if filter_dict is not None and len(filter_dict) > 0:
            query = query.filter_by(**filter_dict)

        if sort is not None:
            # sort is expected to be something like: name,-description,id,+email
            sort_args = [
                desc(v.strip()[1:]) if v.startswith('-') else
                v.strip()[1:] if v.startswith('+') else
                v.strip()
                for v in sort.split(',')]
            query = query.order_by(*sort_args)

        query = query.offset(offset).limit(limit)

        return query

    def create_by_model_name(self, model_name, accepted_keys, **fields):
        values = extract_dict(fields, extracted_keys=accepted_keys)
        model = self.get_model_instance(model_name, **values)
        self.put(model)
        self.commit()
        return model

    def read_by_model_name(self, model_name, pid, **kwargs):
        model_class = self.get_model_class(model_name)
        return model_class.query.get_or_404(pid)

    def update_by_model_name(self, model_name, pid, accepted_keys, pid_key='id', **kwargs):
        values = extract_dict(kwargs, extracted_keys=accepted_keys)
        self.get_model_class(model_name).query.filter_by(**{pid_key: pid}).update(values)
        self.commit()
        return self.read_by_model_name(model_name, pid)  # TODO(hoatle): avoid this?

    def delete_by_model_name(self, model_name, pid, **kwargs):
        model = self.read_by_model_name(model_name, pid, **kwargs)
        self.delete(model)
        self.commit()


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
