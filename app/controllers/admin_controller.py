from flask import Blueprint, request, jsonify
from app.services.admin_service import AdminService
from app.schemas.department_schema import DepartmentSchema
from app.schemas.doctor_schema import DoctorOnboardSchema, DoctorAssignmentSchema
from app.security.decorators import token_required, roles_required
from marshmallow import ValidationError
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_service = AdminService()
logger = logging.getLogger(__name__)

@admin_bp.route('/departments', methods=['POST'])
@token_required
@roles_required('admin')
def create_department():
    json_data = request.json
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = DepartmentSchema().load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    success, message, dept = admin_service.create_department(data)
    if success:
        return jsonify({'message': message, 'department': DepartmentSchema().dump(dept)}), 201
    return jsonify({'message': message}), 409

@admin_bp.route('/departments', methods=['GET'])
@token_required
@roles_required('admin')
def list_departments():
    departments = admin_service.list_departments()
    return jsonify(DepartmentSchema(many=True).dump(departments)), 200

@admin_bp.route('/doctors', methods=['POST'])
@token_required
@roles_required('admin')
def onboard_doctor():
    json_data = request.json
    try:
        data = DoctorOnboardSchema().load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    success, message, doctor = admin_service.onboard_doctor(data)
    if success:
        return jsonify({'message': message, 'doctor_id': doctor.id}), 201
    return jsonify({'message': message}), 409

@admin_bp.route('/assign-doctor', methods=['POST'])
@token_required
@roles_required('admin')
def assign_doctor():
    json_data = request.json
    try:
        data = DoctorAssignmentSchema().load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    success, message = admin_service.assign_doctor_to_department(data['doctor_id'], data['department_id'])
    if success:
        return jsonify({'message': message}), 200
    return jsonify({'message': message}), 400
