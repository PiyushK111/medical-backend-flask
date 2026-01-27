# User, Role, and Authentication models

from enum import Enum as PyEnum
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import db, TimestampMixin

if TYPE_CHECKING:
    from app.models.doctor import DoctorAvailability
    from app.models.appointment import Appointment

class UserRole(str, PyEnum):
    """User roles in the system."""
    ADMIN = "admin"
    DOCTOR = "doctor"
    MEMBER = "member"

class User(TimestampMixin, db.Model):
    """
    User model representing all users (Admin, Doctor, Member).
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.MEMBER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    availabilities: Mapped[List["DoctorAvailability"]] = relationship(
        "DoctorAvailability",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )
    
    appointments_as_patient: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        foreign_keys="Appointment.patient_id",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    appointments_as_doctor: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        foreign_keys="Appointment.doctor_id",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }
