import json
from tache import Tache
from collections import defaultdict
import os.path

user_dict = defaultdict(list)
user_dict2 = defaultdict(list)

def from_json(obj_dict):
    global user_dict2
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Tache":
            obj = Tache(obj_dict["name"], obj_dict["description"], obj_dict["timestamp"], obj_dict["owner"])
            user_dict2[obj_dict["owner"]].append(obj)
    return obj_dict

def to_json(obj):
    if isinstance(obj, Tache):
        return {"__class__": "Tache",
        "name": obj.name,
        "description": obj.description,
        "timestamp" : obj.timestamp,
        "owner" : obj.owner}

def new(owner, title, description, date):
    user_dict[owner].append(Tache(title,description,date,owner))

def update(owner, title, description, date):
    user_dict[owner] = Tache(title,description,date,owner)

def store():
    with open('TasksList.json', 'w', encoding='utf-8') as f:
        json.dump(user_dict, f, indent=4, default=to_json)
        
def load():
    with open("TasksList.json", "r", encoding="utf-8") as fichier:
        json.load(fichier, object_hook=from_json)
#TESTS
userid =  '12341'
userid2 =  '97983'
userid3 =  '32812'

user_dict[userid].append(Tache("Hello","description",1496259221,userid))
user_dict[userid].append(Tache("Manger","description",1496259221,userid))
user_dict[userid2].append(Tache("Dormir","description",1496259221,userid2))
user_dict[userid2].append(Tache("Se laver","description",1496259221,userid2))

store()
load()
print(user_dict)
print("\n")
print(user_dict2)
print(user_dict2[userid][0].name)
print(user_dict2[userid][1].name)
user_dict2[userid3].append(Tache("regarder la tele","description",1496259221,userid2))
print(user_dict2[userid2][0].name)
print(user_dict2[userid2][1].name)
store()
load()
print(user_dict2)
