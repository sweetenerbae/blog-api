from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Reaction
from app.schemas.reaction import ReactionSchema

reaction_ns = Namespace('reactions', description='Реакции на посты')

# Swagger модель
reaction_model = reaction_ns.model('Reaction', {
    'emoji': fields.String(required=True, description='Эмодзи реакции')
})

# Marshmallow схема
reaction_schema = ReactionSchema()
reactions_schema = ReactionSchema(many=True)


@reaction_ns.route('/posts/<int:post_id>')
class ReactionListResource(Resource):
    @jwt_required()
    @reaction_ns.expect(reaction_model)
    def post(self, post_id):
        """Добавить реакцию к посту"""
        data = request.get_json()
        user_id = get_jwt_identity()['id']

        existing = Reaction.query.filter_by(post_id=post_id, user_id=user_id).first()
        if existing:
            return {"msg": "You already reacted to this post"}, 400

        reaction = Reaction(emoji=data['emoji'], post_id=post_id, user_id=user_id)
        db.session.add(reaction)
        db.session.commit()
        return reaction_schema.dump(reaction), 201


@reaction_ns.route('/<int:reaction_id>')
class ReactionResource(Resource):
    @jwt_required()
    def delete(self, reaction_id):
        """Удалить реакцию"""
        reaction = Reaction.query.get_or_404(reaction_id)
        user = get_jwt_identity()

        if reaction.user_id != user['id'] and user['role'] != 'admin':
            return {"msg": "Forbidden"}, 403

        db.session.delete(reaction)
        db.session.commit()
        return {"msg": "Reaction deleted"}, 200