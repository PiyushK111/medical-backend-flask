from marshmallow import Schema, fields, validate

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(dump_only=True)
    doctor_id = fields.Int(required=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(dump_only=True) # Calculated by backend based on slot duration
    status = fields.Str(dump_only=True)
    reason = fields.Str(validate=validate.Length(max=255))
    
    patient_name = fields.Str(dump_only=True)
    doctor_name = fields.Str(dump_only=True)
