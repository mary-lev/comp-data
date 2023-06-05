class Identifiable_entity:
    id: str

    def __init__(self, id):
        self.id=id

    def getId(self):
        return self.id

class Image(Identifiable_entity):
    pass 

class Annotation(Identifiable_entity):
    motivation: str
    body: image
    target: Identifiable_entity
    
    def __init__(self, id, motivation):
        self.motivation = motivation
        
        super().__init__(id)

    def getBody(self):
        return self.image
    
    def getmotivation(self):
        return self.motivation

    def getTarget (self):
        return Identifiable_entity
    

class Entity_with_Metadata(Identifiable_entity):
    label: str
    title: str = None
    creators: list = []

    def __init__(self, id, label, title, creators):
        self.label=label
        self.title=title
        self.creators=creators

        super().__init__(id)

    def getlabel(self):
        return self.label
    
    def gettitle(self):
        return self.title
    
    def getcreators(self):
        return self.creators
    

class Collection(Entity_with_Metadata):
    list_of_manifests: list = []
    
    def getItems(self):
        return self.list_of_manifests



class Manifest(Entity_with_Metadata):
    list_of_canvas: list = []

    def getItems(self):
        return self.list_of_canvas

class Canvas(Entity_with_Metadata):
    pass

