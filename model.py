from typing import List


class IdentifiableEntity:
    id: str

    def __init__(self, id):
        self.id = id

    def getId(self):
        return self.id


class Image(IdentifiableEntity):
    pass


class Annotation(IdentifiableEntity):
    motivation: str
    body: Image
    target: str

    def __init__(self, id, motivation, body, target):
        self.motivation = motivation
        self.target = target
        self.body = body

        super().__init__(id)

    def getBody(self):
        return self.body

    def getMotivation(self):
        return self.motivation

    def getTarget(self):
        return self.target


class EntityWithMetadata(IdentifiableEntity):
    label: str
    title: str = None
    creators: list = []

    def __init__(self, id, label, title=None, creators=None):
        self.label = label
        self.title = title
        if isinstance(creators, str) and creators != "":
            self.creators = creators.split("; ")
        elif isinstance(creators, list):
            self.creators = creators
        else:
            self.creators = []

        super().__init__(id)

    def getLabel(self):
        return self.label

    def getTitle(self):
        return self.title

    def getCreators(self):
        return self.creators


class Canvas(EntityWithMetadata):
    pass


class Manifest(EntityWithMetadata):
    list_of_canvas: List[Canvas] = []

    def __init__(self, id, label, title=None, creators=None, list_of_canvas=None):
        if isinstance(list_of_canvas, list):
            self.list_of_canvas = list_of_canvas
        else:
            self.list_of_canvas = []

        super().__init__(id, label, title, creators)

    def getItems(self):
        return self.list_of_canvas


class Collection(EntityWithMetadata):
    list_of_manifests: List[Manifest] = []

    def __init__(self, id, label, title=None, creators=None, list_of_manifests=None):
        if isinstance(list_of_manifests, list):
            self.list_of_manifests = list_of_manifests
        super().__init__(id, label, title, creators)

    def getItems(self):
        return self.list_of_manifests
