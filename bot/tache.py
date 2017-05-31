class Tache:
    
    def __init__(self, name, description, timestamp, owner):
        self._name = name
        self._description = description
        self._timestamp = timestamp
        self._owner = owner
       
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
        
    @property
    def timestamp(self):
        return self._timestamp
        
    @property
    def owner(self):
        return self._owner
    
    @property
    def fileName(self):
        return f"{self._owner}.json"
        
    def to_json(self):
    #code from http://sdz.tdct.org/sdz/serialisez-vos-objets-au-format-json.html
        return {"__class__": "Tache",
                "name": self._name,
                "description": self._description,
                "timestamp" : self._timestamp,
                "owner" : self._owner}
        
    @staticmethod
    def from_json(obj_dict):
    #code from http://sdz.tdct.org/sdz/serialisez-vos-objets-au-format-json.html
        if "__class__" in obj_dict:
            if obj_dict["__class__"] == "Tache":
                obj = Tache(obj_dict["name"], obj_dict["description"], obj_dict["timestamp"], obj_dict["owner"])
                return obj
        return obj_dict
        
