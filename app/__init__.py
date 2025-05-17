from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config  # ты можешь создать свой config.py

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Расширения
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Регистрация blueprints
    from app.routes.auth import auth_bp
    from app.routes.posts import post_bp
    from app.routes.comments import comment_bp
    from app.routes.reactions import reaction_bp
    from app.routes.user import user_bp  # админские действия

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(post_bp, url_prefix='/api/posts')
    app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(reaction_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api/users')

    return app