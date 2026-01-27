from enum import Enum as PyEnum
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Date, Time, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import db, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class AppointmentStatus(str, PyEnum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Appointment(TimestampMixin, db.Model):
    """Appointment model linking Patient and Doctor."""
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, nullable=False
    )
    
    reason: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    patient: Mapped["User"] = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")
    doctor: Mapped["User"] = relationship("User", foreign_keys=[doctor_id], back_populates="appointments_as_doctor")

    # Constraint: A doctor cannot be double-booked at the exact same start time on the same date.
    __table_args__ = (
        UniqueConstraint('doctor_id', 'date', 'start_time', name='uniq_doctor_date_start'),
    )

    def __repr__(self):
        return f"<Appointment {self.id} {self.date} {self.start_time}>"

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "patient_name": self.patient.name if self.patient else "Unknown",
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor.name if self.doctor else "Unknown",
            "date": self.date.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "status": self.status.value,
            "reason": self.reason
        }
