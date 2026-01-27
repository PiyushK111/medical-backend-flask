from flask import Blueprint, request, jsonify, g # Correction
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.services.appointment_service import AppointmentService
from app.schemas.appointment_schema import AppointmentSchema
from app.security.decorators import token_required, roles_required
from app.models.user import UserRole
import logging

appointment_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')
appointment_service = AppointmentService()
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

logger = logging.getLogger(__name__)

@appointment_bp.route('', methods=['POST'])
@token_required
@roles_required(UserRole.MEMBER.value)
def book_appointment():
    """
    Book an appointment.
    Only Members can book appointments.
    """
    try:
        data = request.get_json()
        validated_data = appointment_schema.load(data)
        
        patient_id = g.user_id # From token
        appointment = appointment_service.book_appointment(patient_id, validated_data)
        
        return jsonify(appointment_schema.dump(appointment)), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as e:
        logger.warning(f"Booking Conflict/Error for user {g.user_id}: {str(e)}")
        # Check if it's a conflict or bad request based on message? 
        return jsonify({"message": str(e)}), 409 # Conflict/Logic Error
    except IntegrityError:
        logger.error(f"Database Integrity Error for user {g.user_id}")
        return jsonify({"message": "Appointment slot already taken."}), 409
    except Exception as e:
        logger.error(f"System Error: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500

@appointment_bp.route('', methods=['GET'])
@token_required
def get_appointments():
    """
    Get appointments.
    - Admins see all.
    - Doctors see theirs.
    - Members see theirs.
    """
    user_id = g.user_id
    role = g.role
    
    appointments = appointment_service.get_appointments_for_user(user_id, role)
    return jsonify(appointments_schema.dump(appointments)), 200
