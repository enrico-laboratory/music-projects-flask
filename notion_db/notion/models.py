from datetime import datetime

class ChoirNotionModel:
    
    def __init__(self,
                 id: str,
                 name: str):
        
        self.id = id
        self.name = name
        
    def __repr__(self) -> str:
        return f'(ChoirNotionModel : "id": {self.id}, "name": {self.name})'

class ContactNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 role: str,
                 email1: str,
                 email2: str = None,
                 address: str = None,
                 phone: str = None,
                 notes: str = None,
                 voice: str = None):

        self.id = id
        self.name = name
        self.role = role
        self.email1 = email1
        self.email2 = email2
        self.address = address
        self.phone = phone
        self.notes = notes
        self.voice = voice

    def __repr__(self) -> str:
        return f'(ContactNotionModel : "id": {self.id}, "name": {self.name}, "role": {self.role}, "email1": {self.email1})'

class LocationNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 city: str,
                 address: str = None,
                 purpose: str = None):

        self.id = id
        self.name = name
        self.city = city
        self.address = address
        self.purpose = purpose

    def __repr__(self) -> str:
        return f'(LocationNotionModel : "id": {self.id}, "name": {self.name}, "city": {self.city}, "address": {self.address}, "purpose": {self.purpose})'

class MusicProjectNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 year: int,
                 choir_id: str = None,
                 status: str = None,
                 excerpt: str = None,
                 description: str = None):

        self.id = id
        self.name = name
        self.year = year
        self.choir_id = choir_id
        self.status = status
        self.excerpt = excerpt
        self.description = description

    def __repr__(self) -> str:
        return f'(MusicProjectNotionModel : "id": {self.id}, "name": {self.name}, "year": {self.year}, "choir_id": {self.choir_id}, "status": {self.status})'

class MusicNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 composer: str,
                 voices: str = None,
                 instruments: str = None,
                 solo: str = None,
                 length: float = None,
                 score: str = None,
                 media: str = None,
                 recording: str = None):

        self.id = id
        self.name = name
        self.composer = composer
        self.voices = voices
        self.instruments = instruments
        self.solo = solo
        self.length = length
        self.score = score
        self.media = media
        self.recording = recording

    def __repr__(self) -> str:
        return f'(MusicNotionModel : "id": {self.id}, "name": {self.name}, "composer": {self.composer}'




class TasksNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 type: int,
                 start_date_time: datetime,
                 end_date_time: datetime,
                 music_project_id: str,
                 location_id: str = None):

        self.id = id
        self.name = name
        self.type = type
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.music_project_id = music_project_id
        self.location_id = location_id

    def __repr__(self) -> str:
        return f'(TasksNotionModel : "id": {self.id}, "name": {self.name}, "type": {self.type}, "start_date": {self.start_date_time}, "end_date_time": {self.end_date_time}, "music_project_id": {self.music_project_id})'

class RoleNotionModel:
    
    def __init__(self,
                 id: str,
                 name: str,
                 music_project_id: int,
                 contact_id: int,
                 note: str,
                 status:str):

        self.id = id
        self.name = name
        self.music_project_id = music_project_id
        self.contact_id = contact_id
        self.note = note
        self.status = status

class PartAllocationNotionModel:

    def __init__(self,
                 id: str,
                 name: str,
                 music_id: int,
                 music_project_id: int,
                 staff_1: str,
                 staff_2: str,
                 staff_3: str,
                 staff_4: str,
                 staff_5: str,
                 staff_6: str,
                 staff_7: str,
                 staff_8: str,
                 staff_9: str,
                 staff_10: str,
                 staff_11: str,
                 staff_12: str,
                 notes: str,
                 selected: bool):

        self.id = id
        self.name = name
        self.music_id = music_id
        self.music_project_id = music_project_id
        self.staff_1 = staff_1
        self.staff_2 = staff_2
        self.staff_3 = staff_3
        self.staff_4 = staff_4
        self.staff_5 = staff_5
        self.staff_6 = staff_6
        self.staff_7 = staff_7
        self.staff_8 = staff_8
        self.staff_9 = staff_9
        self.staff_10 = staff_10
        self.staff_11 = staff_11
        self.staff_12 = staff_12
        self.notes = notes
        self.selected = selected
           