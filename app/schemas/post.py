from marshmallow import Schema, fields

class PostSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    author_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_published = fields.Bool()