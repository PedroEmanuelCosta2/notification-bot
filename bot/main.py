import json
from tache import Tache
from collections import defaultdict
import os.path

user_dict = defaultdict(list)

def handleTask(tache):
    if(os.path.isfile(tache.fileName)):
        #le fichier existe
        with open(tache.fileName, 'w', encoding='utf-8') as f:
            json.dumps(tache.__dict__,f)
    else:
        #le fichier n'existe pas
        print("le fichier n'existe pas")

#meme fonction que celle de la classe
def to_json(obj):
    if isinstance(obj, Tache):
        return {"__class__": "Tache",
                "name": obj.name,
                "description": obj.description,
                "timestamp" : obj.timestamp,
                "owner" : obj.owner}
    raise TypeError(repr(obj) + " n'est pas sérialisable !")

def new(owner, title, description, date):
    user_dict[owner].append(Tache(title,description,date,owner))

def store():
    with open('Test.json', 'w', encoding='utf-8') as f:
        json.dump(user_dict, f, indent=4, default=to_json)


#user_dict2 = defaultdict(list)

# with open("Test.json", "r", encoding="utf-8") as fichier:
#     user_dict2 = json.load(fichier, object_hook=Tache.from_json)
# print(user_dict2)
# print(user_dict[userid][0].name)
# print(user_dict[userid][1].name)
# print(user_dict[userid2][0].name)
# print(user_dict[userid2][1].name)
