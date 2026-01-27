from typing import List, Optional
from app.models.base import db
from app.models.doctor import DoctorAvailability

class AvailabilityRepository:
    @staticmethod
    def create(availability: DoctorAvailability) -> DoctorAvailability:
        db.session.add(availability)
        db.session.commit()
        return availability

    @staticmethod
    def find_by_doctor_id(doctor_id: int) -> List[DoctorAvailability]:
        return db.session.execute(
            db.select(DoctorAvailability).filter_by(doctor_id=doctor_id)
        ).scalars().all()

    @staticmethod
    def find_by_doctor_and_day(doctor_id: int, day_of_week: int) -> Optional[DoctorAvailability]:
        return db.session.execute(
            db.select(DoctorAvailability).filter_by(doctor_id=doctor_id, day_of_week=day_of_week)
        ).scalars().first()

    @staticmethod
    def delete(availability: DoctorAvailability) -> None:
        db.session.delete(availability)
        db.session.commit()
