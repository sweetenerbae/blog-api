import os

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = 10800