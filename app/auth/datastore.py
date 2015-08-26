from abc import abstractmethod, ABCMeta
from datetime import datetime

from flask_security.utils import encrypt_password

from ..datastore import SQLAlchemyDatastore
from ..utils import fix_docs


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

    # @abstractmethod
    # def find_roles_from_user(self, user_id, q=None, filters=None, sort=None, offset=None,
    #                          limit=None, **kwargs):
    #     pass
    #
    # @abstractmethod
    # def add_role_to_user(self, role, user):
    #     """Adds an existing role to an existing user
    #     .. versionadded:: 0.1.0
    #
    #     :param role: the existing role
    #     :param user: the existing user
    #     """
    #     pass
    #
    # @abstractmethod
    # def remove_role_from_user(self, role, user):
    #     """Remove an existing role from an existing user
    #     .. versionadded:: 0.1.0
    #
    #     :param role: the existing role
    #     :param user: the existing user
    #     """
    #     pass

@fix_docs
class SQLAlchemyAuthDatastore(SQLAlchemyDatastore, AuthDatastore):
    """
    Implementation for AuthDataStore with SQLAlchemy
    """
    # User
    def find_users(self, q=None, filters=None, **kwargs):
        accepted_filter_keys = ('email', 'active')
        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('user', **kwargs)

    def create_user(self, **kwargs):
        accepted_keys = ('email', 'password', 'active', 'confirmed_at')
        kwargs['password'] = encrypt_password(kwargs['password'])
        # TODO(hoatle): implement verification by signals
        kwargs['active'] = True
        kwargs['confirmed_at'] = datetime.utcnow()
        user = self.create_by_model_name('user', accepted_keys, **kwargs)
        user.roles.append(self.find_roles(name='user').first())
        self.commit()
        return user

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

    # def find_roles_from_user(self, user_id, q=None, filters=None, sort=None, offset=None,
    #                          limit=None, **kwargs):
    #     # TODO
    #     pass
    #
    # def add_role_to_user(self, role, user):
    #     user.roles.add(role)
    #     self.commit()
    #
    # def remove_role_from_user(self, role, user):
    #     user.roles.pop(role)
    #     self.commit()
