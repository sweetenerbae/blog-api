from app import create_app, db
from app.models import User, UserRole
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    if not User.query.filter_by(role=UserRole.admin).first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash("admin123", method="pbkdf2:sha256"),
            role=UserRole.admin,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created")
    else:
        print("⚠️ Admin already exists")