import json
from tache import Tache

#code inspired from http://sdz.tdct.org/sdz/serialisez-vos-objets-au-format-json.html
def from_json(obj_dict):
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Tache":
            obj = Tache(obj_dict["name"], obj_dict["description"], obj_dict["timestamp"], obj_dict["owner"])
            return obj
    return obj_dict

def to_json(obj):
    if isinstance(obj, Tache):
        return {"__class__": "Tache",
        "name": obj.name,
        "description": obj.description,
        "timestamp" : obj.timestamp,
        "owner" : obj.owner}