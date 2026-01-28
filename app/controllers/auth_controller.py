from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginSchema, RegisterSchema
from app.utils.response import success_response, error_response, validation_error_handler
from marshmallow import ValidationError
import logging

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService()
logger = logging.getLogger(__name__)

@auth_bp.route('/registerUser', methods=['POST'])
def register():
    """
    Register a new user (patient).
    
    Expected constraints:
    - Email must be unique
    - Password requirements met by schema
    """
    try:
        json_data = request.json or {}
        data = RegisterSchema().load(json_data)
        
        success, message, user = auth_service.register_user(data)
        if success:
            logger.info(f"User registered successfully: {user.id}")
            return success_response(
                data={'user_id': user.id}, 
                message=message, 
                status_code=201
            )
        
        logger.warning(f"Registration failed: {message}")
        return error_response(message=message, status_code=409)

    except ValidationError as err:
        return validation_error_handler(err)
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)

@auth_bp.route('/loginUser', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    """
    try:
        json_data = request.json or {}
        data = LoginSchema().load(json_data)

        success, message, token = auth_service.login_user(data)
        if success:
            logger.info(f"User logged in successfully")
            return success_response(
                data={'token': token},
                message=message,
                status_code=200
            )
        
        logger.warning(f"Login failed: {message}")
        return error_response(message=message, status_code=401)

    except ValidationError as err:
        return validation_error_handler(err)
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)
