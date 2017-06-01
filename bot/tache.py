class Tache:

    def __init__(self, name, description, timestamp, owner):
        self.name = name
        self.description = description
        self.timestamp = timestamp
        self.owner = owner
        self.fileName = owner + ".json"

    def to_json(self):
    #code from http://sdz.tdct.org/sdz/serialisez-vos-objets-au-format-json.html
        return {"__class__": "Tache",
                "name": self.name,
                "description": self.description,
                "timestamp" : self.timestamp,
                "owner" : self.owner}

    @staticmethod
    def from_json(obj_dict):
    #code from http://sdz.tdct.org/sdz/serialisez-vos-objets-au-format-json.html
        if "__class__" in obj_dict:
            if obj_dict["__class__"] == "Tache":
                obj = Tache(obj_dict["name"], obj_dict["description"], obj_dict["timestamp"], obj_dict["owner"])
                return obj
        return obj_dict
