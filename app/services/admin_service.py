from typing import List, Tuple, Optional
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.models.department import Department
from app.models.user import User, UserRole
from app.models.doctor import DoctorDepartment
from app.models.base import db
from app.security.utils import hash_password

class AdminService:
    def __init__(self):
        self.department_repository = DepartmentRepository()
        self.user_repository = UserRepository()

    def create_department(self, data: dict) -> Tuple[bool, str, Optional[Department]]:
        if self.department_repository.get_by_name(data['name']):
            return False, "Department already exists", None
        
        department = self.department_repository.create(**data)
        return True, "Department created", department

    def list_departments(self) -> List[Department]:
        return self.department_repository.get_all()

    def onboard_doctor(self, data: dict) -> Tuple[bool, str, Optional[User]]:
        existing_user = self.user_repository.get_by_email(data['email'])
        if existing_user:
            return False, "User already exists", None

        # Force role to DOCTOR
        data['role'] = UserRole.DOCTOR
        data['password_hash'] = hash_password(data.pop('password'))
        
        doctor = self.user_repository.create(**data)
        return True, "Doctor onboarded", doctor

    def assign_doctor_to_department(self, doctor_id: int, department_id: int) -> Tuple[bool, str]:
        doctor = self.user_repository.get_by_id(doctor_id)
        department = self.department_repository.get_by_id(department_id)

        if not doctor or doctor.role != UserRole.DOCTOR:
            return False, "Invalid doctor"
        
        if not department:
            return False, "Invalid department"

        # Check if already assigned (naive check, better to have a repository method)
        # For simplicity in this assignment, we'll just try to add. 
        # Ideally, we should check for existence first to avoid uniques errors if any.
        
        assignment = DoctorDepartment(doctor_id=doctor_id, department_id=department_id)
        db.session.add(assignment)
        try:
            db.session.commit()
            return True, "Doctor assigned to department"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
