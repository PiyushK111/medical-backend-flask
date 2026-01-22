# Medical Departments

from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import db, TimestampMixin

if TYPE_CHECKING:
    from app.models.doctor import DoctorDepartment


class Department(TimestampMixin, db.Model):
    """
    Department model representing medical departments.

    Departments help organize doctors and appointments.
    """

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    doctor_assignments: Mapped[List["DoctorDepartment"]] = relationship(
        "DoctorDepartment",
        back_populates="department",
        lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<Department {self.name}>"

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
