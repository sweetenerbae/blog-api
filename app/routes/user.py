from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.schemas.user import UserSchema
from app.utils.decorators import role_required

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users))

@user_bp.route('/<int:user_id>/activate', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def activate_user(user_id):
    print("➡️ reached activate_user()")
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    return jsonify({"msg": f"User {user.username} activated"}), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"})

@user_bp.route('/debug/users', methods=['GET'])
def debug_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role.value,
        "is_active": u.is_active
    } for u in users])

@user_bp.route('/debug/me', methods=['GET'])
@jwt_required()
def get_me():
    identity = get_jwt_identity()
    print("🧠 Me:", identity)
    return jsonify(identity)