from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    name = fields.String(required=True)
    # Role is optional during registration (defaults to MEMBER), unless admin sets it
    role = fields.String(validate=validate.OneOf(["admin", "doctor", "member"]))
