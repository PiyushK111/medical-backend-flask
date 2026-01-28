from flask import Blueprint, request, g
from marshmallow import ValidationError
from app.services.availability_service import AvailabilityService
from app.schemas.availability_schema import DoctorAvailabilitySchema
from app.security.decorators import token_required, roles_required
from app.models.user import UserRole
from app.utils.response import success_response, error_response, validation_error_handler
import logging

availability_bp = Blueprint('availability', __name__, url_prefix='/api/availability')
availability_service = AvailabilityService()
availability_schema = DoctorAvailabilitySchema()
availabilities_schema = DoctorAvailabilitySchema(many=True)

logger = logging.getLogger(__name__)

@availability_bp.route('/updateAvailability', methods=['POST'])
@token_required
@roles_required(UserRole.DOCTOR.value)
def create_or_update_availability():
    """
    Create or update doctor availability.
    Only Doctors can manage their own availability.
    """
    try:
        data = request.get_json() or {}
        validated_data = availability_schema.load(data)
        
        doctor_id = g.user_id # From token
        availability = availability_service.create_availability(doctor_id, validated_data)
        
        logger.info(f"Availability updated for doctor {doctor_id}")
        return success_response(
            data=availability_schema.dump(availability),
            message="Availability updated successfully",
            status_code=200
        )
    except ValidationError as err:
        return validation_error_handler(err)
    except Exception as e:
        logger.error(f"Error creating availability for doctor {g.user_id}: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)

@availability_bp.route('/getDoctorAvailability/<int:doctor_id>', methods=['GET'])
@token_required
def get_availability(doctor_id):
    """
    Get availability for a specific doctor.
    Accessible by all authenticated users.
    """
    try:
        availabilities = availability_service.get_doctor_availability(doctor_id)
        return success_response(
            data=availabilities_schema.dump(availabilities),
            message="Availability retrieved successfully",
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error retrieving availability for doctor {doctor_id}: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)

@availability_bp.route('/getMyAvailability', methods=['GET'])
@token_required
@roles_required(UserRole.DOCTOR.value)
def get_my_availability():
    """
    Get current logged-in doctor's availability.
    """
    try:
        doctor_id = g.user_id
        availabilities = availability_service.get_doctor_availability(doctor_id)
        return success_response(
            data=availabilities_schema.dump(availabilities),
            message="Your availability retrieved successfully",
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error retrieving availability for doctor {g.user_id}: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)
