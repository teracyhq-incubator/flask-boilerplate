from abc import abstractmethod, ABCMeta

from sqlalchemy import desc
import inflection

from ..datastore import SQLAlchemyDatastore
from ..utils import extract_dict, add_filters


class AuthDatastore(object):
    """Abstract IoradDatastore class.

    .. versionadded:: 0.1.0
    """

    __metaclass__ = ABCMeta

    # users

    @abstractmethod
    def find_users(self, q=None, filters=None, sort=None, offset=None, limit=None, **kwargs):
        """Find all existing users from the datastore
        by optional query and options.

        .. versionadded:: 0.1.0

        :param q: the optional query as a string which is provided by
                      the current user, default is None.
        :param filters: the filters list of directory item with keys: (key, op, value)
        :param sort: sorting string (sort='+a,-b,c')
        :param offset: offset (integer positive)
        :param limit: limit (integer positive)
        :param kwargs: the additional keyword arguments containing filter dict {key:value,}

        :return the query
        """
        pass

    @abstractmethod
    def create_user(self, **kwargs):
        """Creates a new user associated with the current user then save it to the database.

        .. versionadded:: 0.1.0

        :param kwargs: the optional kwargs
        :return the created user
        """
        pass

    @abstractmethod
    def read_user(self, pid, **kwargs):
        """Reads an existing user associated with the current user by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an user.
        :param kwargs: the optional kwargs.

        :return the found user
        """
        pass

    @abstractmethod
    def update_user(self, pid, **kwargs):
        """Updates an existing user associated with the current user by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an user.
        :param kwargs: the optional kwargs.

        :return the updated user
        """
        pass

    @abstractmethod
    def delete_user(self, pid, **kwargs):
        """Deletes a existing user associated with the current user by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an user.
        :param kwargs: the optional kwargs
        """
        pass

    # roles
    @abstractmethod
    def find_roles(self, q=None, filters=None, sort=None, offset=None, limit=None, **kwargs):
        """Search the list of all existing roles from the database
        by optional query and optional filter.

        .. versionadded:: 0.1.0

        :param q: the optional query as a string which is provided by
                      the current user, default is None.
        :param filters: the filters list of directory item with keys: (key, op, value)
        :param sort: sorting string (sort='+a,-b,c')
        :param offset: offset
        :param limit: limit
        :param kwargs: the additional keyword arguments containing filter dict {key:value,}

        :return the query
        """
        pass

    @abstractmethod
    def create_role(self, **kwargs):
        """Creates a new role associated with the current user then save it to the database.

        .. versionadded:: 0.1.0

        :param kwargs: the optional kwargs

        :return the created role.
        """
        pass

    @abstractmethod
    def read_role(self, pid, **kwargs):
        """Reads an existing role associated with the current user by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an user.
        :param kwargs: the optional kwargs

        :return the found role
        """
        pass

    @abstractmethod
    def update_role(self, pid, **kwargs):
        """Updates an existing user associated with the current user by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an user.
        :param kwargs: the optional kwargs

        :return the updated role.
        """
        pass

    @abstractmethod
    def delete_role(self, pid, **kwargs):
        """Deletes a existing user associated with the current user by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an user.
        :param kwargs: the optional kwargs
        """
        pass


class SQLAlchemyAuthDatastore(SQLAlchemyDatastore, AuthDatastore):
    """
    Implementation for AuthDataStore with SQLAlchemy
    """

    def __init__(self, db):
        SQLAlchemyDatastore.__init__(self, db)
        # dynamic create model_registry
        # thanks to:
        # http://stackoverflow.com/questions/26514823/get-all-models-from-flask-sqlalchemy-db
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

    # User

    def find_users(self, q=None, filters=None, **kwargs):
        accepted_filter_keys = ('first_name', 'last_name', 'email', 'public_name', 'active',
                                'type_id', 'language_id', 'license_id', 'status', 'is_subscribed',
                                'is_deleted')
        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('user', **kwargs)

    def create_user(self, **kwargs):
        accepted_keys = ('email', 'first_name', 'last_name', 'public_name', 'password',
                         'logo_image_name')
        return self.create_by_model_name('user', accepted_keys, **kwargs)

    def read_user(self, pid, **kwargs):
        return self.read_by_model_name('user', pid, **kwargs)

    def update_user(self, pid, **kwargs):
        return self.update_by_model_name('user', pid, **kwargs)

    def delete_user(self, pid, **kwargs):
        self.delete_by_model_name('user', pid, **kwargs)

    # Role
    def find_roles(self, q=None, filters=None, **kwargs):
        # TODO(hoatle): add this meta into Model instead?
        accepted_filter_keys = ('name', 'description')

        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('role', **kwargs)

    def create_role(self, **kwargs):
        accepted_keys = ('name', 'description')
        return self.create_by_model_name('role', accepted_keys, **kwargs)

    def read_role(self, pid, **kwargs):
        return self.read_by_model_name('role', pid, **kwargs)

    def update_role(self, pid, **kwargs):
        accepted_keys = ('name', 'description')
        return self.update_by_model_name('role', pid, accepted_keys)

    def delete_role(self, pid, **kwargs):
        self.delete_by_model_name('role', pid, **kwargs)
