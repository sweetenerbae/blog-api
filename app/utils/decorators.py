from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            jwt_data = get_jwt()
            user_role = jwt_data.get('role')

            print("🧠 role:", user_role)
            print("🧠 id:", get_jwt_identity())

            if user_role not in roles:
                return jsonify({"msg": "Access denied: insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
