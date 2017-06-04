import json
from tache import Tache
from collections import defaultdict
from math import ceil
import os.path

user_dict = defaultdict(list)

def from_json(obj_dict):
    global user_dict2
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Tache":
            obj = Tache(obj_dict["name"], obj_dict["description"], obj_dict["time"], obj_dict["owner"])
            user_dict[obj_dict["owner"]].append(obj)
    return obj_dict

def to_json(obj):
    if isinstance(obj, Tache):
        return {"__class__": "Tache",
        "name": obj.name,
        "description": obj.description,
        "time" : obj.time,
        "owner" : obj.owner}

def new(owner, title, description, date):
    #TODO Test all args dateFormat for date
    user_dict[owner].append(Tache(title,description,date,owner))
    #return str

def delete(owner, id_u):
    d = ceil(int(id_u))
    name = user_dict[owner][d].name
    del user_dict[owner][d]
    return f"La tâche : {name} a bien été supprimée !"

def update(owner,id_u,attributeUpdated,newValue):
    try:
        d=ceil(int(id_u))
        name = user_dict[owner][d].name
        attributeLow = attributeUpdated.lower()
        if(len(user_dict[owner])>0 and d>=0 and d<len(user_dict[owner])):
            if attributeLow=='name':
                user_dict[owner][d]=Tache(newValue,user_dict[owner][d].description,user_dict[owner][d].time,owner)
                strResult=f"Tache {name} modifiée avec succès"
            elif attributeLow=='description':
                user_dict[owner][d]=Tache(user_dict[owner][d].name,newValue,user_dict[owner][d].time,owner)
                strResult=f"Tache {name} modifiée avec succès"
            elif attributeLow=='time' :
                #TODO
                #convert time
                #change next line
                user_dict[owner][d]=Tache(user_dict[owner][d].name,user_dict[owner][d].description,user_dict[owner][d].time,owner)
                strResult=f"Tache {name} modifiée avec succès"
            else:
                strResult="Champ inexistant Essayez :name | description | time"
        else:
            strResult="Numéro de tache non valide.\n?list pour voir le tache disponible."
    except ValueError:
        strResult="Le numéro de tache doit être une valeur numérique"
    return strResult

def listTask(owner):
    if len(user_dict[owner])>0 :
        strResult=f"Voici la liste de vos taches :\n\n"
        i=0
        for tache in user_dict[owner]:
            strResult +=f"\t{i}\t{tache.name}\n"
            i+=1
    else:
        strResult=f"Vous n'avez actuellement aucune tâche, créer en une avec ?new"
    return strResult

def dateFormat(StrDate):
    #TODO check if date format is valid
    return true

def helpTask():
    return f"Liste des commandes :\n\n\tCreate a new task :\n\t?new \"Name\" \"Description\" \"Date\"\n\n\tChange one attribute of a task : \n\t?update \"name | description | time\" \"new value\"\n\n\tObtain the list of all your tasks :\n\t?list\n\n\tObtain the details of a task :\n\t?detail tasknumber\n\n\tDelete a task :\n\t?delete tasknumber"

def detail(owner,id):
    try:
        d=ceil(int(id))
        if(len(user_dict[owner])>0 and d>=0 and d<len(user_dict[owner])):
            strResult=f"Détails de la tache {d} :\n\tDescription :\n\t\t{user_dict[owner][d].description}\n\tDate du rappel:\n\t\t{user_dict[owner][d].time}\ncette tache peut à tout moment être éditée grace à la commande ?update."
        else:
            strResult="Numéro de tache non valide.\n?list pour voir le tache disponible."
    except ValueError:
        strResult="Veuillez entrer un valeur numérique"
    return strResult

# def callback(name, date):
#     print(f"RAPPEL ! Il est temps ({date}) de faire votre tâche : {name}")

# def dateToTimestamp(date_str):
#
#
# def timestampToDate(date_float):


def store():
    try:
        with open('TasksList.json', 'w', encoding='utf-8') as f:
            json.dump(user_dict, f, indent=4, default=to_json)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

def load():
    try:
        with open("TasksList.json", "r", encoding="utf-8") as fichier:
            json.load(fichier, object_hook=from_json)
    except IOError as e:
        #nothing will be loaded
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
