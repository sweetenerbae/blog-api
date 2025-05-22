from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import User, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

auth_ns = Namespace('auth', description='Аутентификация')

register_model = auth_ns.model('Register', {
    'username': fields.String(required=True, example='student1'),
    'email': fields.String(required=True, example='student1@example.com'),
    'password': fields.String(required=True, example='password123'),
    'role': fields.String(required=True, example='student', enum=['teacher', 'student']),
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, example='admin@example.com'),
    'password': fields.String(required=True, example='admin123'),
})

token_model = auth_ns.model('Token', {
    'access_token': fields.String(example='eyJhbGciOi...')
})

message_model = auth_ns.model('Message', {
    'msg': fields.String
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'Успешная регистрация', model=message_model)
    @auth_ns.response(400, 'Неверные данные', model=message_model)
    def post(self):
        data = request.get_json()

        if data['role'] not in ('teacher', 'student'):
            return {"msg": "Role must be teacher or student"}, 400

        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return {"msg": "Username or email already exists"}, 400

        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'], method='pbkdf2:sha256'),
            role=UserRole(data['role']),
            is_active=False,
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        return {"msg": "User registered. Wait for admin activation."}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Успешный вход', model=token_model)
    @auth_ns.response(401, 'Неверные учетные данные', model=message_model)
    @auth_ns.response(403, 'Аккаунт не активирован', model=message_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password_hash, data['password']):
            return {'msg': 'Invalid credentials'}, 401

        if not user.is_active:
            return {'msg': 'Account not activated'}, 403

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role.value},
            expires_delta=timedelta(hours=3)
        )
        return {'access_token': token}, 200