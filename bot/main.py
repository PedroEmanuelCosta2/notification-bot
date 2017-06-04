import json
from tache import Tache
from collections import defaultdict
from datetime import datetime
from math import ceil
import os.path

user_dict = defaultdict(list)

def from_json(obj_dict):
    """Permet d'ajouter toutes les tâches stockées dans le json dans le dictionnaire user_dict."""
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Tache":
            obj = Tache(obj_dict["name"], obj_dict["description"], obj_dict["time"], obj_dict["owner"])
            user_dict[obj_dict["owner"]].append(obj)
    return obj_dict

def to_json(obj):
    """Sérialise les objets Tache du dictionaire sous format json."""
    if isinstance(obj, Tache):
        return {"__class__": "Tache",
        "name": obj.name,
        "description": obj.description,
        "time" : obj.time,
        "owner" : obj.owner}

def new(owner, title, description, date):
    """Ajoute une tâche au dictionaire."""
    try:
        dateTask = datetime.strptime(date,"%d/%m/%Y %H:%M")
        user_dict[owner].append(Tache(title,description,date,owner))
        return f"La tâche : {title} a bien été créée et vous sera rappelée le {date} !"
    except:
        return f"Création de tache impossible, vous devez absolument respecter le format de date suivant :\n\t \"dd\\mm\\yyyy hh:mm\""

def delete(owner, id_u):
    """Supprime la tâche selon l'indice en paramètre."""
    try:
        d = ceil(int(id_u))
        name = user_dict[owner][d].name
        del user_dict[owner][d]
        return f"La tâche : {name} a bien été supprimée !"
    except:
        return f"Impossible de supprimer la tâche : {name}"

def update(owner,id_u,attributeUpdated,newValue):
    """Met à jour la tâche en indice selon l'argument donné et sa nouvelle valeur."""
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
                try:
                    dateTask = datetime.strptime(newValue,"%d/%m/%Y %H:%M")
                    user_dict[owner][d]=Tache(user_dict[owner][d].name,user_dict[owner][d].description,newValue,owner)
                    strResult=f"Tache {name} modifiée avec succès"
                except:
                   strResult="Mise a jour de la tache impossible, vous devez absolument respecter le format de date suivant :\n\t \"dd/mm/yyyy hh:mm\""
            else:
                strResult="Champ inexistant Essayez :name | description | time"
        else:
            strResult="Numéro de tache non valide.\nlist pour voir le tache disponible."
    except ValueError:
        strResult="Le numéro de tache doit être une valeur numérique"
    return strResult

def listTask(owner):
    """Liste les tâches de l'utilisteur."""
    if len(user_dict[owner])>0 :
        strResult=f"Voici la liste de vos taches :\n\n"
        i=0
        for tache in user_dict[owner]:
            strResult +=f"\t{i}\t{tache.name}\n"
            i+=1
    else:
        strResult=f"Vous n'avez actuellement aucune tâche, créer en une avec new"
    return strResult

def helpTask():
    """Affiche les commandes disponibles sur le bot."""
    return f"Liste des commandes :\n\n\tCreate a new task :\n\tnew \"Name\" \"Description\" \"Date\"\n\n\tChange one attribute of a task : \n\tupdate \"name | description | time\" \"new value\"\n\n\tObtain the list of all your tasks :\n\tlist\n\n\tObtain the details of a task :\n\tdetail tasknumber\n\n\tDelete a task :\n\tdelete tasknumber"

def detail(owner,id):
    """Affiche les détails d'une tâche."""
    try:
        d=ceil(int(id))
        if(len(user_dict[owner])>0 and d>=0 and d<len(user_dict[owner])):
            strResult=f"Détails de la tache {d} :\n\tDescription :\n\t\t{user_dict[owner][d].description}\n\tDate du rappel:\n\t\t{user_dict[owner][d].time}\ncette tache peut à tout moment être éditée grace à la commande ?update."
        else:
            strResult="Numéro de tache non valide.\nlist pour voir le tache disponible."
    except ValueError:
        strResult="Veuillez entrer un valeur numérique"
    return strResult


def store():
    """Stocke toutes les tâches dans le fichier json."""
    try:
        with open('TasksList.json', 'w', encoding='utf-8') as f:
            json.dump(user_dict, f, indent=4, default=to_json)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

def load():
    """Récupère toutes les tâches du fichier json."""
    try:
        with open("TasksList.json", "r", encoding="utf-8") as fichier:
            json.load(fichier, object_hook=from_json)
    except IOError as e:
        #nothing will be loaded
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
