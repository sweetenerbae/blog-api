from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Post
from app.schemas.post import PostSchema

post_ns = Namespace('posts', description='Операции со статьями')

post_model = post_ns.model('Post', {
    'title': fields.String(required=True, description='Post title'),
    'content': fields.String(required=True, description='Post content'),
})

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@post_ns.route('')
class PostList(Resource):
    @post_ns.expect(post_model)
    @post_ns.response(201, 'Post created')
    @post_ns.doc(security='Bearer')
    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data:
            return {"msg": "Invalid JSON"}, 400

        user_id = get_jwt_identity()
        post = Post(
            title=data['title'],
            content=data['content'],
            author_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        return {'post': post_schema.dump(post)}, 201

    @post_ns.response(200, 'Success')
    def get(self):
        posts = Post.query.filter_by(is_published=True)\
                          .order_by(Post.updated_at.desc())\
                          .all()
        return posts_schema.dump(posts), 200

@post_ns.route('/<int:post_id>')
class PostResource(Resource):
    @post_ns.response(200, 'Success')
    @post_ns.response(404, 'Post not found')
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        if not post.is_published:
            return {'msg': 'Post is hidden'}, 404
        return post_schema.dump(post)

    @post_ns.expect(post_model)
    @post_ns.response(200, 'Post updated')
    @post_ns.response(403, 'Forbidden')
    @post_ns.response(404, 'Post not found')
    @post_ns.doc(security='Bearer')
    @jwt_required()
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        user = get_jwt_identity()

        if user['id'] != post.author_id and user['role'] != 'admin':
            return {'msg': 'Forbidden'}, 403

        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post_schema.dump(post), 200

    @post_ns.response(200, 'Post deleted')
    @post_ns.response(403, 'Forbidden')
    @post_ns.response(404, 'Post not found')
    @post_ns.doc(security='Bearer')
    @jwt_required()
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        user = get_jwt_identity()

        if user['id'] != post.author_id and user['role'] != 'admin':
            return {'msg': 'Forbidden'}, 403

        db.session.delete(post)
        db.session.commit()
        return {'msg': 'Post deleted'}, 200