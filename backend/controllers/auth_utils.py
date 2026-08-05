from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify


def role_required(required_roles):
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in required_roles:
                return jsonify({"message": "You do not have access to this resource."}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
