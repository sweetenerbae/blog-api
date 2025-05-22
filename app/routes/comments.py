from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Comment
from app.schemas.comment import CommentSchema
from app.utils.decorators import role_required

comment_ns = Namespace('comments', description='Комментарии')

comment_model = comment_ns.model('Comment', {
    'content': fields.String(required=True, description='Текст комментария')
})

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

@comment_ns.route('/<int:comment_id>')
class CommentResource(Resource):
    @jwt_required()
    def delete(self, comment_id):
        """Удаление комментария (только автор или админ)"""
        comment = Comment.query.get_or_404(comment_id)
        user = get_jwt_identity()
        if comment.author_id != user['id'] and user['role'] != 'admin':
            return {"msg": "Forbidden"}, 403
        db.session.delete(comment)
        db.session.commit()
        return {"msg": "Комментарий удалён"}, 200


@comment_ns.route('/posts/<int:post_id>')
class PostCommentListResource(Resource):
    @jwt_required()
    @role_required('student', 'teacher')
    @comment_ns.expect(comment_model)
    def post(self, post_id):
        """Создание комментария к посту"""
        data = request.get_json()
        user_id = get_jwt_identity()['id']
        comment = Comment(text=data['content'], author_id=user_id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201

    def get(self, post_id):
        """Получение всех комментариев к посту"""
        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments_schema.dump(comments), 200