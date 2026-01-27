from marshmallow import Schema, fields, validate

class DoctorAvailabilitySchema(Schema):
    id = fields.Int(dump_only=True)
    doctor_id = fields.Int(dump_only=True)
    day_of_week = fields.Int(required=True, validate=validate.Range(min=0, max=6))
    start_time = fields.Str(required=True, validate=validate.Regexp(r'^\d{2}:\d{2}$'))
    end_time = fields.Str(required=True, validate=validate.Regexp(r'^\d{2}:\d{2}$'))
    slot_duration_minutes = fields.Int(load_default=30, validate=validate.Range(min=15, max=60))
    is_active = fields.Bool(load_default=True)
    day_name = fields.Method("get_day_name", dump_only=True)

    def get_day_name(self, obj):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[obj.day_of_week]
