import jwt
import datetime
from flask import current_app
from typing import Dict, Any, Optional

def generate_token(user_id: int, role: str) -> str:
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=0),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_id),
            'role': role
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY', 'default_secret_key_change_me'),
            algorithm='HS256'
        )
    except Exception as e:
        import traceback
        import logging
        logging.error(f"JWT Generation Error: {str(e)}")
        logging.error(traceback.format_exc())
        return f"Error generating token: {str(e)}"

def decode_token(auth_token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(
            auth_token,
            current_app.config.get('SECRET_KEY', 'default_secret_key_change_me'),
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        import logging
        logging.error(f"Token Expired: {e}")
        return None
    except jwt.InvalidTokenError as e:
        import logging
        logging.error(f"Token Invalid: {e}")
        return None
