"""
use this command to run this file:

$ python manage.py db seed
"""

from app.auth.models import Role


def run():
    Role.insert_roles()
