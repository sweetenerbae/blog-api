from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.schemas.user import UserSchema
from app.utils.decorators import role_required

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('', methods=['GET'])  # /api/users
@jwt_required()
@role_required('admin')
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@user_bp.route('/<int:user_id>/activate', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    return jsonify({"msg": "User activated"})

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"})