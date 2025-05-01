from marshmallow import Schema, fields
from marshmallow.validate import ContainsOnly


class PlainChoirSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainContactSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    role = fields.Str()
    email1 = fields.Str()
    email2 = fields.Str()
    address = fields.Str()
    phone = fields.Str()
    address = fields.Str()
    notes = fields.Str()
    voice = fields.Str()


class PlainLocationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    city = fields.Str()
    address = fields.Str()
    purpose = fields.Str(validate=[ContainsOnly(['Rehearsal', 'Concert'])])


class PlainMusicSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    composer = fields.Str()
    voices = fields.Str()
    instruments = fields.Str()
    solo = fields.Str()
    length = fields.Float()
    score = fields.Url()
    media = fields.Url()
    recording = fields.Url()


class PlainMusicProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    year = fields.Int()
    status = fields.Str()
    excerpt = fields.Str()
    description = fields.Str()
    choir = fields.Nested(PlainChoirSchema(), dump_only=True)


class PlainPartAllocationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    staff_1 = fields.Str()
    staff_2 = fields.Str()
    staff_3 = fields.Str()
    staff_4 = fields.Str()
    staff_5 = fields.Str()
    staff_6 = fields.Str()
    staff_7 = fields.Str()
    staff_8 = fields.Str()
    staff_9 = fields.Str()
    staff_10 = fields.Str()
    staff_11 = fields.Str()
    staff_12 = fields.Str()
    notes = fields.Str()
    selected = fields.Bool()
    music = fields.Nested(PlainMusicSchema(), dump_only=True)
    music_project = fields.Nested(PlainMusicProjectSchema(), dump_only=True, only=["id","name"])


class PlainRoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    note = fields.Str()
    status = fields.Str()
    contact = fields.Nested(PlainContactSchema(), dump_only=True)
    music_project = fields.Nested(PlainMusicProjectSchema(), dump_only=True, only=['choir', 'id','name'])



class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    start_date_time = fields.DateTime()
    end_date_time = fields.DateTime()
    type = fields.Str()
    music_project = fields.Nested(PlainMusicProjectSchema(), dump_only=True, only=['choir', 'id','name'])
    location = fields.Nested(PlainLocationSchema(), dump_only=True)
