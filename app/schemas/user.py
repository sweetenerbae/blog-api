from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    role = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()