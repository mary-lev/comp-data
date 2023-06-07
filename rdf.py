# all the classes for handling RDF database
from processor import Processor
from json import load
import json
from rdflib import RDF, Literal, URIRef, Graph
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore, SPARQLStore
from rdflib.namespace import RDFS
from pymantic import sparql


class CollectionProcessor(Processor):

    def uploadData(self, filename):
        server = sparql.SPARQLServer(self.dbPathOrUrl)
        q = "drop graphs"
        server.update(q)
        # URIRef for classes
        collection = URIRef("http://iiif.io/api/presentation/3#Collection")
        manifest = URIRef("http://iiif.io/api/presentation/3#Manifest")
        canvas = URIRef("http://iiif.io/api/presentation/3#Canvas")

        has_item = URIRef("http://iiif.io/api/presentation/3#hasItem")

        my_graph = Graph()

        with open(filename, "r") as user_file:
            json_file = json.load(user_file)

            for key, value in json_file.items():

                collection_subject = URIRef(json_file["id"])
                print("Subject: ", collection_subject)

                if key == "type" and value == "Collection":
                    type_triple = (collection_subject, RDF.type, collection)
                    my_graph.add(type_triple)
                    label = Literal(json_file["label"]["none"][0])
                    label_triple = (collection_subject, RDFS.label, label)
                    my_graph.add(label_triple)

                    print("Items: ", len(json_file["items"]))
                    for item in json_file["items"]:
                        print(item["type"])
                        if item["type"] == "Manifest":
                            manifest_subject = URIRef(item["id"])
                            type_triple = (manifest_subject, RDF.type, manifest)
                            my_graph.add(type_triple)
                            label = Literal(item["label"]["none"][0])
                            print("Manifest label: ", label)
                            label_triple = (manifest_subject, RDFS.label, label)
                            my_graph.add(label_triple)
                            triple = (collection_subject, has_item, manifest_subject)
                            my_graph.add(triple)

                            for each in item["items"]:
                                print(each.keys())
                                if each["type"] == "Canvas":
                                    canvas_subject = URIRef(each["id"])
                                    type_triple = (canvas_subject, RDF.type, canvas)
                                    my_graph.add(type_triple)
                                    label = Literal(each["label"]["none"][0])
                                    print("Label of canvas: ", label)
                                    label_triple = (canvas_subject, RDFS.label, label)
                                    my_graph.add(label_triple)
                                    triple = (manifest_subject, has_item, canvas_subject)
                                    my_graph.add(triple)
           
            store = SPARQLUpdateStore()

            store.open((self.dbPathOrUrl, self.dbPathOrUrl))
            for triple in my_graph.triples((None, None, None)):
                store.add(triple)
                print("Added triple: ", triple)
            store.close()


grp_endpoint = "http://127.0.0.1:9999/blazegraph/sparql"
col_dp = CollectionProcessor()
col_dp.setDbPathOrUrl(grp_endpoint)
col_dp.uploadData("data/collection-1.json")
col_dp.uploadData("data/collection-2.json")


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
