from typing import List
from app.models.doctor import DoctorAvailability
from app.repositories.availability_repository import AvailabilityRepository
import logging

logger = logging.getLogger(__name__)

class AvailabilityService:
    """
    Service for managing doctor availability slots.
    """
    def __init__(self):
        self.repository = AvailabilityRepository()

    def create_availability(self, doctor_id: int, data: dict) -> DoctorAvailability:
        """
        Creates or updates availability for a doctor on a specific day.
        
        Args:
            doctor_id (int): ID of the doctor
            data (dict): Availability details (day_of_week, start_time, end_time, etc.)
            
        Returns:
            DoctorAvailability: The created or updated availability object
        """
        # Check if slot already exists for this day
        existing = self.repository.find_by_doctor_and_day(doctor_id, data['day_of_week'])
        
        if existing:
            # Update existing
            existing.start_time = data['start_time']
            existing.end_time = data['end_time']
            existing.slot_duration_minutes = data.get('slot_duration_minutes', 30)
            existing.is_active = data.get('is_active', True)
            self.repository.create(existing) # save (add/commit)
            logger.info(f"Availability updated for Doctor {doctor_id} on day {data['day_of_week']}")
            return existing

        availability = DoctorAvailability(
            doctor_id=doctor_id,
            day_of_week=data['day_of_week'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            slot_duration_minutes=data.get('slot_duration_minutes', 30),
            is_active=data.get('is_active', True)
        )
        created = self.repository.create(availability)
        logger.info(f"Availability created for Doctor {doctor_id} on day {data['day_of_week']}")
        return created

    def get_doctor_availability(self, doctor_id: int) -> List[DoctorAvailability]:
        """
        Retrieves all availability slots for a doctor.
        """
        return self.repository.find_by_doctor_id(doctor_id)
