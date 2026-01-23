from functools import wraps
from flask import request, jsonify, g
from app.security.jwt import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Bearer token malformed'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        # Store user info in flask global 'g' object for access in controllers
        g.user_id = payload.get('sub')
        g.role = payload.get('role')

        return f(*args, **kwargs)

    return decorated

def roles_required(*roles):
    """
    Decorator to check if user has one of the required roles.
    Must be used AFTER @token_required.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'role'):
                return jsonify({'message': 'Authentication required first'}), 401
            
            if g.role not in roles:
                return jsonify({'message': 'Permission denied'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
