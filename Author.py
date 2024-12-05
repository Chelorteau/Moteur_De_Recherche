class Author:
    def __init__(self , name, ndoc, production = {}):
        self.name = name
        self.ndoc = ndoc
        self.production = production

    def add(self, production, id):
        self.production[id] = production
        self.ndoc += 1

    def __str__(self):
        return f"Auteur : {self.name} a écrit {self.ndoc} documents"
    
