class Tache:
    
    def __init__(self, name, description, timestamp, owner):
        self._name = name
        self._description = description
        self._timestamp = timestamp
        self._owner = owner
        self._fileName = owner + ".json"
       
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
        return self._fileName
