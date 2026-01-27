
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import db, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.department import Department

class DoctorDepartment(TimestampMixin, db.Model):
    """Association table linking doctors to departments."""
    __tablename__ = "doctor_departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable=False)

    doctor: Mapped["User"] = relationship("User")
    department: Mapped["Department"] = relationship("Department", back_populates="doctor_assignments")


class DoctorAvailability(TimestampMixin, db.Model):
    """Doctor's available time slots."""
    __tablename__ = "doctor_availabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time: Mapped[str] = mapped_column(String(5), nullable=False)  # "09:00"
    end_time: Mapped[str] = mapped_column(String(5), nullable=False)    # "17:00"
    slot_duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    doctor: Mapped["User"] = relationship("User", back_populates="availabilities")

    def __repr__(self) -> str:
        return f"<Availability Doctor:{self.doctor_id} Day:{self.day_of_week}>"

    def to_dict(self) -> dict:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "day_of_week": self.day_of_week,
            "day_name": days[self.day_of_week],
            "start_time": self.start_time,
            "end_time": self.end_time,
            "slot_duration_minutes": self.slot_duration_minutes,
            "is_active": self.is_active
        }
