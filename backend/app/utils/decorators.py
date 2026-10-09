from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_roles = claims.get('roles', [])
            if not any(role in allowed_roles for role in user_roles):
                return jsonify({'error': 'Acceso denegado: permisos insuficientes'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
