from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(*roles):
    """
    Декоратор проверяет, что у пользователя одна из допустимых ролей.
    Пример: @role_required('admin'), @role_required('teacher', 'admin')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            identity = get_jwt_identity()
            user_role = identity.get('role')

            if user_role not in roles:
                return jsonify({"msg": "Access denied: insufficient permissions"}), 403

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper