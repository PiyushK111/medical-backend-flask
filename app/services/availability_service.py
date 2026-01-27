from typing import List
from app.models.doctor import DoctorAvailability
from app.repositories.availability_repository import AvailabilityRepository

class AvailabilityService:
    def __init__(self):
        self.repository = AvailabilityRepository()

    def create_availability(self, doctor_id: int, data: dict) -> DoctorAvailability:
        # Check if slot already exists for this day (simple logic: one slot per day per doctor for now, as per simple requirement interpretation or we can allow multiple if logic permits)
        # Requirement said: "Doctors can create, update, delete their availability"
        # Let's check for existing availability on that day to prevent duplicates or update it.
        # For simplicity in this assignment, let's assume one availability block per day.
        
        existing = self.repository.find_by_doctor_and_day(doctor_id, data['day_of_week'])
        if existing:
            # Update existing
            existing.start_time = data['start_time']
            existing.end_time = data['end_time']
            existing.slot_duration_minutes = data.get('slot_duration_minutes', 30)
            existing.is_active = data.get('is_active', True)
            self.repository.create(existing) # save (add/commit)
            return existing

        availability = DoctorAvailability(
            doctor_id=doctor_id,
            day_of_week=data['day_of_week'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            slot_duration_minutes=data.get('slot_duration_minutes', 30),
            is_active=data.get('is_active', True)
        )
        return self.repository.create(availability)

    def get_doctor_availability(self, doctor_id: int) -> List[DoctorAvailability]:
        return self.repository.find_by_doctor_id(doctor_id)
