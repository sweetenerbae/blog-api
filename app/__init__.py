from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

# Инициализация расширений
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Инициализация API-инстанса (вынесен для использования в models/schemas)
    api = Api(
        title="teachers-blog API",
        version="1.0",
        description="Блог преподавателей факультета с REST API на Flask",
        doc="/docs"  # Swagger UI доступен по /docs
    )

    from app.routes.auth import auth_ns
    from app.routes.user import user_ns
    from app.routes.posts import post_ns
    from app.routes.comments import comment_ns
    from app.routes.reactions import reaction_ns

    # Регистрация namespace'ов через API
    api.init_app(app)
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(user_ns, path="/api/users")
    api.add_namespace(comment_ns, path="/api/comments")
    api.add_namespace(reaction_ns, path="/api/reactions")
    api.add_namespace(post_ns, path="/api/posts")

    return app