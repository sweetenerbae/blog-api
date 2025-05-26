from flask_restx import Namespace, Resource, fields
from flask import request
from sqlalchemy import func
from app.models import Post, Comment
from app.schemas.post import PostSchema

feed_ns = Namespace('feed', description='Лента последних статей')

post_model = feed_ns.model('Post', {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'created_at': fields.DateTime,
})

@feed_ns.route('/')
class FeedResource(Resource):
    @feed_ns.doc(
        description="Получить список последних статей с комментариями",
        params={
            'page': 'Номер страницы (по умолчанию 1)',
            'per_page': 'Количество постов на странице (по умолчанию 10)',
            'q': 'Поиск по заголовку или содержимому',
            'sort': 'Сортировка: date | likes | comments (по умолчанию date)'
        }
    )
    @feed_ns.marshal_list_with(post_model)
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('q')
        sort = request.args.get('sort', 'date')

        query = Post.query

        if search:
            query = query.filter(
                Post.title.ilike(f'%{search}%') |
                Post.content.ilike(f'%{search}%')
            )

        if sort == 'likes':
            query = query.order_by(Post.likes_count.desc())
        elif sort == 'comments':
            query = query.outerjoin(Comment).group_by(Post.id).order_by(func.count(Comment.id).desc())
        else:  # sort == 'date' or unknown
            query = query.order_by(Post.created_at.desc())

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        posts = paginated.items

        return PostSchema(many=True).dump(posts), 200