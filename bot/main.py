import json
from tache import *
import os.path

def checkIfFileExist(fname):
    if(os.path.isfile(fname)):
        return True
    else:
        return False

def handleTask(tache):
    if(checkIfFileExist(tache.fileName)):
        print("le fichier existe")
        with open(tache.fileName, 'w', encoding='utf-8') as f:
            json.dumps(tache.__dict__,f)
    else:
        print("le fichier n'existe pas : " + tache.fileName )
        
def serializer(obj):
#code from http://sdz.tdct.org/sdz/serialisez-vos-objets-au-format-json.html
    if isinstance(obj, Tache):
        return {"__class__": "Tache",
                "name": obj.name,
                "description": obj.description,
                "timestamp" : obj.timestamp,
                "owner" : obj.owner}
    raise TypeError(repr(obj) + " is not serializable")

def deserializer(obj_dict):
#code from http://sdz.tdct.org/sdz/serialisez-vos-objets-au-format-json.html
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Tache":
            obj = Tache(obj_dict["name"], obj_dict["description"], obj_dict["timestamp"], obj_dict["owner"])
            return obj
    return objet

        
tache =  Tache("Hello","description",12031212,"paul")
dict = serializer(tache)
tache =  deserializer(dict)
print(tache.fileName)
with open("paul.json", "w", encoding="utf-8") as file:
    json.dump(tache, file, default=serializer)
with open("paul.json", "r", encoding="utf-8") as file:
    tache = json.load(file, object_hook=deserializer)
print(tache.fileName)
