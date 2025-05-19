from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Post
from app.schemas.post import PostSchema
from app.utils.decorators import role_required

post_bp = Blueprint('post_bp', __name__)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@post_bp.route('/posts', methods=['POST'])
@jwt_required()
@role_required('teacher')
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    post = Post(title=data['title'], content=data['content'], author_id=user_id)
    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post), 201

@post_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return posts_schema.jsonify(posts), 200

@post_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post_schema.jsonify(post)

@post_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = get_jwt_identity()
    if user['id'] != post.author_id and user['role'] != 'admin':
        return jsonify({"msg": "Forbidden"}), 403
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return post_schema.jsonify(post)

@post_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = get_jwt_identity()
    if user['id'] != post.author_id and user['role'] != 'admin':
        return jsonify({"msg": "Forbidden"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Пост удален"})