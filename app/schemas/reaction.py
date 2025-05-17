from marshmallow import Schema, fields

class ReactionSchema(Schema):
    id = fields.Int()
    emoji = fields.Str(required=True)
    post_id = fields.Int()
    user_id = fields.Int()