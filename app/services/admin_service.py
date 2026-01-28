from typing import List, Tuple, Optional
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.models.department import Department
from app.models.user import User, UserRole
from app.models.doctor import DoctorDepartment
from app.models.base import db
from app.security.utils import hash_password
import logging

logger = logging.getLogger(__name__)

class AdminService:
    """
    Service for administrative tasks like managing departments and doctors.
    """
    def __init__(self):
        self.department_repository = DepartmentRepository()
        self.user_repository = UserRepository()

    def create_department(self, data: dict) -> Tuple[bool, str, Optional[Department]]:
        """
        Creates a new department.
        
        Args:
            data (dict): Department data (name, etc.)
            
        Returns:
            Tuple[bool, str, Optional[Department]]: (success, message, department_obj)
        """
        if self.department_repository.get_by_name(data['name']):
            logger.warning(f"Create department failed: Already exists ({data['name']})")
            return False, "Department already exists", None
        
        department = self.department_repository.create(**data)
        logger.info(f"Department created: {department.name}")
        return True, "Department created", department

    def list_departments(self) -> List[Department]:
        """
        Lists all departments.
        
        Returns:
            List[Department]: List of all departments
        """
        return self.department_repository.get_all()

    def onboard_doctor(self, data: dict) -> Tuple[bool, str, Optional[User]]:
        """
        Onboards a new doctor.
        
        Args:
            data (dict): Doctor registration data
            
        Returns:
            Tuple[bool, str, Optional[User]]: (success, message, doctor_obj)
        """
        existing_user = self.user_repository.get_by_email(data['email'])
        if existing_user:
            logger.warning(f"Onboard doctor failed: User already exists ({data['email']})")
            return False, "User already exists", None

        # Force role to DOCTOR
        data['role'] = UserRole.DOCTOR
        data['password_hash'] = hash_password(data.pop('password'))
        
        doctor = self.user_repository.create(**data)
        logger.info(f"Doctor onboarded: ID {doctor.id}")
        return True, "Doctor onboarded", doctor

    def assign_doctor_to_department(self, doctor_id: int, department_id: int) -> Tuple[bool, str]:
        """
        Assigns a doctor to a department.
        
        Args:
            doctor_id (int): ID of the doctor
            department_id (int): ID of the department
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        doctor = self.user_repository.get_by_id(doctor_id)
        department = self.department_repository.get_by_id(department_id)

        if not doctor or doctor.role != UserRole.DOCTOR:
            return False, "Invalid doctor"
        
        if not department:
            return False, "Invalid department"

        # Check if already assigned (naive check)
        # Ideally, we should check for existence first to avoid unique constraints error
        
        assignment = DoctorDepartment(doctor_id=doctor_id, department_id=department_id)
        db.session.add(assignment)
        try:
            db.session.commit()
            logger.info(f"Doctor {doctor_id} assigned to department {department_id}")
            return True, "Doctor assigned to department"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to assign doctor {doctor_id} to department {department_id}: {str(e)}")
            return False, str(e)
