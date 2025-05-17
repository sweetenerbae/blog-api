from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Comment
from app.schemas.comment import CommentSchema
from app.utils.decorators import role_required

comment_bp = Blueprint('comment_bp', __name__)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    user = get_jwt_identity()

    # Только автор комментария или админ может удалить
    if comment.author_id != user['id'] and user['role'] != 'admin':
        return jsonify({"msg": "Forbidden"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"msg": "Comment deleted"}), 200

@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
@role_required('student', 'teacher')
def create_comment(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    comment = Comment(text=data['content'], author_id=user_id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return comment_schema.jsonify(comment), 201

@comment_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return comments_schema.jsonify(comments), 200