from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Int()
    content = fields.Str(required=True)
    post_id = fields.Int()
    author_id = fields.Int()
    created_at = fields.DateTime()