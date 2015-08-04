from flask_security import RoleMixin, UserMixin

from ..extensions import db

roles_users = db.Table(
    'role_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable=False),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), nullable=False)
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    @staticmethod
    def insert_roles():
        roles = [
            {'name': 'user', 'description': 'user role'},
            {'name': 'admin', 'description': 'admin role'}
        ]
        for r in roles:
            role = Role.query.filter_by(name=r.get('name')).first()
            if role is None:
                role = Role(**r)
                db.session.add(role)
            db.session.commit()

    def __repr__(self):
        return '<Role(id="%s", name="%s", description="%s")>' % \
               (self.id, self.name, self.description)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
