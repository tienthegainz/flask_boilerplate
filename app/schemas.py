from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=6))
    address = fields.String(required=True)


class UserLoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=6))
