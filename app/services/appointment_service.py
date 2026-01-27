from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.models.appointment import Appointment, AppointmentStatus
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.availability_repository import AvailabilityRepository

class AppointmentService:
    def __init__(self):
        self.appt_repo = AppointmentRepository()
        self.avail_repo = AvailabilityRepository()

    def book_appointment(self, patient_id: int, data: Dict[str, Any]) -> Appointment:
        doctor_id = data['doctor_id']
        appt_date = data['date'] # datetime.date object from marshmallow
        start_time = data['start_time'] # datetime.time object
        
        # 1. Check Doctor Availability
        day_of_week = appt_date.weekday()
        availability = self.avail_repo.find_by_doctor_and_day(doctor_id, day_of_week)
        
        if not availability or not availability.is_active:
             raise ValueError("Doctor is not available on this day.")

        # Check time window
        avail_start = datetime.strptime(availability.start_time, "%H:%M").time()
        avail_end = datetime.strptime(availability.end_time, "%H:%M").time()
        
        if start_time < avail_start:
            raise ValueError(f"Doctor starts at {availability.start_time}")
            
        # Calculate End Time
        slot_minutes = availability.slot_duration_minutes
        # Combine date and time to perform arithmetic
        start_dt = datetime.combine(appt_date, start_time)
        end_dt = start_dt + timedelta(minutes=slot_minutes)
        end_time = end_dt.time()
        
        if end_time > avail_end:
             raise ValueError(f"Appointment exceeds doctor's working hours (ends at {availability.end_time})")

        # 2. Check for Double Booking (Database Level Pre-check)
        conflict = self.appt_repo.find_conflicting_appointment(doctor_id, appt_date, start_time)
        if conflict:
            raise ValueError("Doctor is already booked for this slot.")

        # 3. Create Appointment
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=appt_date,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.SCHEDULED,
            reason=data.get('reason')
        )
        
        return self.appt_repo.create(appointment)

    def get_appointments_for_user(self, user_id: int, role: str) -> List[Appointment]:
        if role == 'admin':
            return self.appt_repo.find_all()
        elif role == 'doctor':
             return self.appt_repo.find_by_doctor(user_id)
        else: # Member/Patient
             return self.appt_repo.find_by_patient(user_id)
