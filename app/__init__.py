from flasgger import Swagger
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'User Auth API',
        'uiversion': 3,
        'specs': [{
            'endpoint': 'apispec',
            'route': '/apispec.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }],
        'static_url_path': '/flasgger_static',
        'specs_route': '/docs/'
    }
    app.config.from_object(Config)

    # Расширения
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    Swagger(app, template_file='docs/swagger_config.yml')

    # Регистрация blueprints
    from app.routes.auth import auth_bp
    from app.routes.posts import post_bp
    from app.routes.comments import comment_bp
    from app.routes.reactions import reaction_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(post_bp, url_prefix='/api/posts')
    app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(reaction_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api/users')

    return app