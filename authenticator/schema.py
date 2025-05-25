from marshmallow import Schema, fields, ValidationError

from models.enums import UserRoleEnum

class EnumField(fields.Field):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        return value.value if value else None

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.enum(value)
        except ValueError:
            raise ValidationError(f"Invalid value. Must be one of: {[e.value for e in self.enum]}")

class UserSchemaRegister(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = EnumField(UserRoleEnum, required=True)

class UserSchemaLogin(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    username = fields.Str(required=True, dump_only=True)
    password = fields.Str(required=True, load_only=True)
    role = EnumField(UserRoleEnum, required=True, dump_only=True)