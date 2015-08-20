from marshmallow import fields

from ..api.schemas import Schema


class PagingSchema(Schema):
    count = fields.Int()
    offset = fields.Int()
    limit = fields.Int()
    previous = fields.Str()
    next = fields.Str()


class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()


class RoleListSchema(Schema):
    data = fields.List(fields.Nested(RoleSchema))
    paging = fields.Nested(PagingSchema)


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    active = fields.Bool()
    confirmed_at = fields.DateTime()
    roles = fields.List(fields.Nested(RoleSchema))


class UserListSchema(Schema):
    data = fields.List(fields.Nested(UserSchema))
    paging = fields.Nested(PagingSchema)
