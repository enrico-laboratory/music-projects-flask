from marshmallow import Schema, fields, EXCLUDE

class TaskSchema(Schema):
    
    name = fields.Str()
    type = fields.Str()
    
    class Meta():
        
        unknown = EXCLUDE