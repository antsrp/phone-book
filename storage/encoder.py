import json

from storage.note import Note

class NoteEncoder(json.JSONEncoder):
    def default(self, v):
        if isinstance(v, Note):
            return {
            'id': v.id,
            'surname': v.surname,
            'name': v.name,
            'patronym': v.patronym,
            'org': v.org,
            'phone_work': v.phone_work,
            'phone_direct': v.phone_direct,
        }
        else:
            return super().default(v)
    
def note_decoder(dict) -> Note:
    return Note(dict["id"], dict["surname"], dict["name"], dict["patronym"], dict["org"], dict["phone_work"], dict["phone_direct"])