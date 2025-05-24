import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def token(app):
    with app.app_context():
        return create_access_token(identity={'id': 1, 'role': 'admin'})