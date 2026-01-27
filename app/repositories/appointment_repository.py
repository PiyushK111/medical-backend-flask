from typing import List, Optional
from datetime import date, time
from app.models.base import db
from app.models.appointment import Appointment, AppointmentStatus

class AppointmentRepository:
    @staticmethod
    def create(appointment: Appointment) -> Appointment:
        db.session.add(appointment)
        db.session.commit()
        return appointment

    @staticmethod
    def find_conflicting_appointment(doctor_id: int, appt_date: date, start_time: time) -> Optional[Appointment]:
        """
        Check if there is already an active (not cancelled) appointment 
        for the doctor at the same date and start time.
        """
        return db.session.execute(
            db.select(Appointment).filter(
                Appointment.doctor_id == doctor_id,
                Appointment.date == appt_date,
                Appointment.start_time == start_time,
                Appointment.status != AppointmentStatus.CANCELLED
            )
        ).scalars().first()

    @staticmethod
    def find_by_patient(patient_id: int) -> List[Appointment]:
        return db.session.execute(
            db.select(Appointment).filter_by(patient_id=patient_id)
        ).scalars().all()

    @staticmethod
    def find_by_doctor(doctor_id: int) -> List[Appointment]:
        return db.session.execute(
            db.select(Appointment).filter_by(doctor_id=doctor_id)
        ).scalars().all()

    @staticmethod
    def find_all() -> List[Appointment]:
        return db.session.execute(db.select(Appointment)).scalars().all()
