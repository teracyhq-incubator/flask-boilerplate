from app.auth.models import Role


def run():
    Role.insert_roles()
