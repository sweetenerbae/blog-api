from flask import Blueprint, request, jsonify
from app import db
from app.models import User, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if data['role'] not in ('teacher', 'student'):
        return jsonify({"msg": "Role must be teacher or student"}), 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({"msg": "Username or email already exists"}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'], method='pbkdf2:sha256'),        role=UserRole(data['role']),
        is_active=False,
        created_at=datetime.utcnow()
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered. Wait for admin activation."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"msg": "Account not activated"}), 403

    token = create_access_token(
        identity={"id": user.id, "role": user.role.value},
        expires_delta=timedelta(hours=3)
    )
    return jsonify(access_token=token), 200