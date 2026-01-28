from flask import Blueprint, request, g
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.services.appointment_service import AppointmentService
from app.schemas.appointment_schema import AppointmentSchema
from app.security.decorators import token_required, roles_required
from app.models.user import UserRole
from app.utils.response import success_response, error_response, validation_error_handler
import logging

appointment_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')
appointment_service = AppointmentService()
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

logger = logging.getLogger(__name__)

@appointment_bp.route('/bookAppointment', methods=['POST'])
@token_required
@roles_required(UserRole.MEMBER.value)
def book_appointment():
    """
    Book an appointment.
    Only Members can book appointments.
    """
    try:
        data = request.get_json() or {}
        validated_data = appointment_schema.load(data)
        
        patient_id = g.user_id # From token
        appointment = appointment_service.book_appointment(patient_id, validated_data)
        
        logger.info(f"Appointment booked for user {patient_id}")
        return success_response(
            data=appointment_schema.dump(appointment),
            message="Appointment booked successfully",
            status_code=201
        )

    except ValidationError as err:
        return validation_error_handler(err)
    except ValueError as e:
        logger.warning(f"Booking Conflict/Error for user {g.user_id}: {str(e)}")
        return error_response(message=str(e), status_code=409)
    except IntegrityError:
        logger.error(f"Database Integrity Error for user {g.user_id}")
        return error_response(message="Appointment slot already taken", status_code=409)
    except Exception as e:
        logger.error(f"System Error: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)

@appointment_bp.route('/getUserAppointments', methods=['GET'])
@token_required
def get_appointments():
    """
    Get appointments.
    - Admins see all.
    - Doctors see theirs.
    - Members see theirs.
    """
    try:
        user_id = g.user_id
        role = g.role
        
        appointments = appointment_service.get_appointments_for_user(user_id, role)
        return success_response(
            data=appointments_schema.dump(appointments),
            message="Appointments retrieved successfully",
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error retrieving appointments for user {g.user_id}: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)
