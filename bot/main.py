import json
from tache import Tache
from collections import defaultdict
from MyJSONParser import from_json, to_json
import os.path

user_dict = defaultdict(list)

def new(owner, title, description, date):
    user_dict[owner].append(Tache(title,description,date,owner))

def update(owner, title, description, date):
    user_dict[owner] = Tache(title,description,date,owner)

def store():
    with open('TasksList.json', 'w', encoding='utf-8') as f:
        json.dump(user_dict, f, indent=4, default=to_json)
        
def load():
    user_dict =defaultdict(list)
    with open("TasksList.json", "r", encoding="utf-8") as fichier:
        user_dict = json.load(fichier, object_hook=from_json)
        return user_dict
#TESTS
userid =  '12341'
userid2 =  '97983'

user_dict[userid].append(Tache("Hello","description",1496259221,userid))
user_dict[userid].append(Tache("Manger","description",1496259221,userid))
user_dict[userid2].append(Tache("Dormir","description",1496259221,userid2))
user_dict[userid2].append(Tache("Se laver","description",1496259221,userid2))

store()
user_dict2 =defaultdict(list)
user_dict2 = load()
print(user_dict)
print("\n")
print(user_dict2)
print(user_dict2[userid][0].name)
print(user_dict2[userid][1].name)
print(user_dict2[userid2][0].name)
print(user_dict2[userid2][1].name)

