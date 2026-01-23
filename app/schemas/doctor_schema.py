from marshmallow import Schema, fields

class DoctorAssignmentSchema(Schema):
    doctor_id = fields.Int(required=True)
    department_id = fields.Int(required=True)

class DoctorOnboardSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    name = fields.String(required=True)
    # Role is implicitly doctor
