from flask import Blueprint, request
from app.services.admin_service import AdminService
from app.schemas.department_schema import DepartmentSchema
from app.schemas.doctor_schema import DoctorOnboardSchema, DoctorAssignmentSchema
from app.security.decorators import token_required, roles_required
from app.utils.response import success_response, error_response, validation_error_handler
from marshmallow import ValidationError
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
admin_service = AdminService()
logger = logging.getLogger(__name__)

@admin_bp.route('/addDepartment', methods=['POST'])
@token_required
@roles_required('admin')
def create_department():
    """
    Create a new department.
    """
    try:
        json_data = request.json or {}
        data = DepartmentSchema().load(json_data)
        
        success, message, dept = admin_service.create_department(data)
        if success:
            logger.info(f"Department created: {dept.name}")
            return success_response(
                data={'department': DepartmentSchema().dump(dept)},
                message=message,
                status_code=201
            )
        return error_response(message=message, status_code=409)

    except ValidationError as err:
        return validation_error_handler(err)
    except Exception as e:
        logger.error(f"Error creating department: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)

@admin_bp.route('/getAllDepartments', methods=['GET'])
@token_required
@roles_required('admin')
def list_departments():
    """
    Get all departments.
    """
    try:
        departments = admin_service.list_departments()
        return success_response(
            data=DepartmentSchema(many=True).dump(departments),
            message="Departments retrieved successfully",
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error listing departments: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)

@admin_bp.route('/onboardDoctor', methods=['POST'])
@token_required
@roles_required('admin')
def onboard_doctor():
    """
    Onboard a new doctor.
    """
    try:
        json_data = request.json or {}
        data = DoctorOnboardSchema().load(json_data)
        
        success, message, doctor = admin_service.onboard_doctor(data)
        if success:
            logger.info(f"Doctor onboarded: {doctor.id}")
            return success_response(
                data={'doctor_id': doctor.id},
                message=message,
                status_code=201
            )
        return error_response(message=message, status_code=409)

    except ValidationError as err:
        return validation_error_handler(err)
    except Exception as e:
        logger.error(f"Error onboarding doctor: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)

@admin_bp.route('/assignDoctorToDepartment', methods=['POST'])
@token_required
@roles_required('admin')
def assign_doctor():
    """
    Assign a doctor to a department.
    """
    try:
        json_data = request.json or {}
        data = DoctorAssignmentSchema().load(json_data)
        
        success, message = admin_service.assign_doctor_to_department(data['doctor_id'], data['department_id'])
        if success:
            logger.info(f"Doctor {data['doctor_id']} assigned to department {data['department_id']}")
            return success_response(message=message, status_code=200)
        return error_response(message=message, status_code=400)

    except ValidationError as err:
        return validation_error_handler(err)
    except Exception as e:
        logger.error(f"Error assigning doctor: {str(e)}")
        return error_response(message="Internal Server Error", status_code=500)
