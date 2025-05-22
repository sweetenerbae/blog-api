from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.utils.decorators import role_required

user_ns = Namespace('users', description='Управление пользователями')

user_model = user_ns.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'role': fields.String,
    'is_active': fields.Boolean
})

@user_ns.route('/')
class UserList(Resource):
    @jwt_required()
    @role_required('admin')
    @user_ns.marshal_list_with(user_model)
    @user_ns.response(200, 'Список пользователей')
    def get(self):
        """Получить список всех пользователей (только для admin)"""
        users = User.query.all()
        return users


@user_ns.route('/<int:user_id>/activate')
class ActivateUser(Resource):
    @jwt_required()
    @role_required('admin')
    @user_ns.response(200, 'Пользователь активирован')
    @user_ns.response(404, 'Пользователь не найден')
    def patch(self, user_id):
        """Активировать пользователя (только для admin)"""
        user = User.query.get_or_404(user_id)
        user.is_active = True
        db.session.commit()
        return {"msg": f"User {user.username} activated"}, 200


@user_ns.route('/<int:user_id>')
class DeleteUser(Resource):
    @jwt_required()
    @role_required('admin')
    @user_ns.response(200, 'Пользователь удалён')
    @user_ns.response(404, 'Пользователь не найден')
    def delete(self, user_id):
        """Удалить пользователя (только для admin)"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"msg": "User deleted"}, 200


@user_ns.route('/debug/users')
class DebugUserList(Resource):
    def get(self):
        """DEBUG: список всех пользователей"""
        users = User.query.all()
        return [{
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role.value,
            "is_active": u.is_active
        } for u in users]


@user_ns.route('/debug/me')
class GetMe(Resource):
    @jwt_required()
    def get(self):
        """DEBUG: получить текущего пользователя"""
        identity = get_jwt_identity()
        return {"user_id": identity}