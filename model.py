class Identifiable_entity:
    id: str

    def __init__(self, id):
        self.id = id

    def getId(self):
        return self.id


class Image(Identifiable_entity):
    pass 


class Annotation(Identifiable_entity):
    motivation: str
    body: Image
    target: Identifiable_entity
    
    def __init__(self, id, motivation, body, target):
        self.motivation = motivation
        self.target = target
        self.body = body
        
        super().__init__(id)

    def getBody(self):
        return self.image
    
    def getMotivation(self):
        return self.motivation

    def getTarget (self):
        return Identifiable_entity
    

class Entity_with_Metadata(Identifiable_entity):
    label: str
    title: str = None
    creators: list = []

    def __init__(self, id, label, title, creators):
        self.label = label
        self.title = title
        self.creators = creators

        super().__init__(id)

    def getLabel(self):
        return self.label
    
    def getTitle(self):
        return self.title
    
    def getCreators(self):
        return self.creators
    

class Canvas(Entity_with_Metadata):
    pass


class Manifest(Entity_with_Metadata):
    list_of_canvas: list = [Canvas]

    def getItems(self):
        return self.list_of_canvas


class Collection(Entity_with_Metadata):
    list_of_manifests: list = [Manifest]
    
    def getItems(self):
        return self.list_of_manifests



canvas = Canvas("http://example.org/canvas1", "canvas", "Canvas 1", ["John Doe"])
manifest = Manifest("http://example.org/manifest1", "manifest", "Manifest 1", ["John Doe"])

print(canvas.getId())
print(manifest.getId())


image = Image("http://example.org/image1")
print(image.getId())

annotation = Annotation("http://example.org/anno1", "painting", image, "http://example.org/canvas1")    
annotation.body = Image("http://example.org/image1")

print(annotation.getId())
print(annotation.getMotivation())
