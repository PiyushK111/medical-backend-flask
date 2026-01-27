from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from app.services.availability_service import AvailabilityService
from app.schemas.availability_schema import DoctorAvailabilitySchema
from app.security.decorators import token_required, roles_required
from app.models.user import UserRole

availability_bp = Blueprint('availability', __name__, url_prefix='/api/availability')
availability_service = AvailabilityService()
availability_schema = DoctorAvailabilitySchema()
availabilities_schema = DoctorAvailabilitySchema(many=True)

@availability_bp.route('', methods=['POST'])
@token_required
@roles_required(UserRole.DOCTOR.value)
def create_or_update_availability():
    """
    Create or update doctor availability.
    Only Doctors can manage their own availability.
    """
    try:
        data = request.get_json()
        validated_data = availability_schema.load(data)
        
        doctor_id = g.user_id # From token
        availability = availability_service.create_availability(doctor_id, validated_data)
        
        return jsonify(availability_schema.dump(availability)), 200 # 200 OK because it might be update
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@availability_bp.route('/<int:doctor_id>', methods=['GET'])
@token_required
def get_availability(doctor_id):
    """
    Get availability for a specific doctor.
    Accessible by all authenticated users.
    """
    availabilities = availability_service.get_doctor_availability(doctor_id)
    return jsonify(availabilities_schema.dump(availabilities)), 200

@availability_bp.route('/me', methods=['GET'])
@token_required
@roles_required(UserRole.DOCTOR.value)
def get_my_availability():
    """
    Get current logged-in doctor's availability.
    """
    doctor_id = g.user_id
    availabilities = availability_service.get_doctor_availability(doctor_id)
    return jsonify(availabilities_schema.dump(availabilities)), 200
