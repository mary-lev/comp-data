# all the classes for handling RDF database
from processor import Processor
from json import load
import json
from rdflib import RDF, Literal, URIRef, Graph
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.namespace import RDFS


# URIRef for classes
Collections = URIRef("http://iiif.io/api/presentation/3#Collection")
Manifest = URIRef("http://iiif.io/api/presentation/3#Manifest")
Canvas = URIRef("http://iiif.io/api/presentation/3#Canvas")

# URIRef for Properties

id = URIRef("https://dl.ficlit.unibo.it/iiif/2/19428/manifest")
# label = URIRef("")
item = URIRef("http://iiif.io/api/presentation/3#hasItem")


my_graph = Graph()


class CollectionProcessor(Processor):
    def __init__(self):
        super().__init__()

    def uploadData(self):

        # with open(path, "r", encoding="utf-8") as g:
        with open('data/collection-2.json') as user_file:
            json_file = json.load(user_file)

            for key, value in json_file.items():
                if key == "id":
                    subject = URIRef(value)

                if key == "type" and value == "Collection":
                    object = URIRef(
                        "http://iiif.io/api/presentation/3#Collection")
                    triple = (subject, RDF.type, object)
                    my_graph.add(triple)

                elif key == "type" and value == "Canvas":
                    object = URIRef("http://iiif.io/api/presentation/3#Canvas")
                    triple = (subject, RDF.type, object)
                    my_graph.add(triple)

                elif key == "type" and value == "Manifest":
                    object = URIRef(
                        "http://iiif.io/api/presentation/3#Manifest")
                    triple = (subject, RDF.type, object)
                    my_graph.add(triple)

                if key == "label":
                    for key, value in value.items():
                        object = Literal(value)
                        triple = (subject, RDFS.label, object)
                        my_graph.add(triple)

                if key == "items":
                    for dict in value:
                        for inner_key, inner_value in dict.items():
                            if inner_key == "id":
                                object = URIRef(inner_value)
                                triple = (subject, URIRef(
                                    "http://iiif.io/api/presentation/3#hasItem"), object)
                                my_graph.add(triple)


Collection_Processor = CollectionProcessor()

Collection_Processor.uploadData('data/collection-2.json')


# upload data to the endpoint


store = SPARQLUpdateStore()

endpoint = "http://172.20.10.2:9999/blazegraph/"

store.open((endpoint, endpoint))
for triple in my_graph.triples((None, None, None)):
    store.add(triple)

    # store.close()


pass


class TriplestoreQueryProcessor(Processor):

    def getAllCanvases():
        """it returns a data frame containing all the canvases included in the database."""
        pass

    def getAllCollections():
        """it returns a data frame containing all the collections included in the database."""
        pass

    def getAllManifests():
        """it returns a data frame containing all the manifests included in the database."""
        pass

    def getCanvasesInCollection():
        """it returns a data frame containing all the canvases included in the database 
        that are contained in the collection identified by the input identifier."""
        pass

    def getCanvasesInManifest():
        """it returns a data frame containing all the canvases included in the database 
        that are contained in the manifest identified by the input identifier."""
        pass

    def getManifestsInCollection():
        """it returns a data frame containing all the manifests included in the database 
        that are contained in the collection identified by the input identifier."""
        pass
