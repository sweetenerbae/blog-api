from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config, TestingConfig

# Расширения
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    # Расширения
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    api = Api(
        title="teachers-blog API",
        version="1.0",
        description="Блог преподавателей факультета с REST API на Flask",
        doc="/docs"
    )

    from app.routes.auth import auth_ns
    from app.routes.user import user_ns
    from app.routes.posts import post_ns
    from app.routes.comments import comment_ns
    from app.routes.reactions import reaction_ns

    api.init_app(app)
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(user_ns, path="/api/users")
    api.add_namespace(comment_ns, path="/api/comments")
    api.add_namespace(reaction_ns, path="/api/reactions")
    api.add_namespace(post_ns, path="/api/posts")

    return app