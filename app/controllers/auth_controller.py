from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginSchema, RegisterSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    json_data = request.json
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    
    try:
        data = RegisterSchema().load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    success, message, user = auth_service.register_user(data)
    if success:
        return jsonify({'message': message, 'user_id': user.id}), 201
    return jsonify({'message': message}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.json
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = LoginSchema().load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    success, message, token = auth_service.login_user(data)
    if success:
        return jsonify({'message': message, 'token': token}), 200
    return jsonify({'message': message}), 401
