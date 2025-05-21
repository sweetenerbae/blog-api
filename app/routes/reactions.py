from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Reaction
from app.schemas.reaction import ReactionSchema
from flasgger import Swagger, swag_from

reaction_bp = Blueprint('reaction_bp', __name__)
reaction_schema = ReactionSchema()
reactions_schema = ReactionSchema(many=True)

@reaction_bp.route('/posts/<int:post_id>/reactions', methods=['POST'])
@jwt_required()
def add_reaction(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()['id']

    # Проверка: уже ставил ли пользователь реакцию
    existing = Reaction.query.filter_by(post_id=post_id, user_id=user_id).first()
    if existing:
        return jsonify({"msg": "You already reacted to this post"}), 400

    reaction = Reaction(emoji=data['emoji'], post_id=post_id, user_id=user_id)
    db.session.add(reaction)
    db.session.commit()
    return reaction_schema.jsonify(reaction), 201

@reaction_bp.route('/reactions/<int:reaction_id>', methods=['DELETE'])
@jwt_required()
def delete_reaction(reaction_id):
    reaction = Reaction.query.get_or_404(reaction_id)
    user = get_jwt_identity()

    if reaction.user_id != user['id'] and user['role'] != 'admin':
        return jsonify({"msg": "Forbidden"}), 403

    db.session.delete(reaction)
    db.session.commit()
    return jsonify({"msg": "Reaction deleted"}), 200