import json
from .tache import Tache
import os.path

def handleTask(tache):
    if(os.path.isfile(tache.fileName)):
        #le fichier existe
        with open(tache.fileName, 'w', encoding='utf-8') as f:
            json.dumps(tache.__dict__,f)
    else:
        print("le fichier n'existe pas : " + tache.fileName )
    
tache =  Tache("Hello","description",12031212,"paul")
dict = to_json(tache)
tache =  from_json(dict)
print(tache.fileName)
with open("paul.json", "w", encoding="utf-8") as file:
    json.dump(tache, file, default=serializer)
with open("paul.json", "r", encoding="utf-8") as file:
    tache = json.load(file, object_hook=deserializer)
print(tache.fileName)
