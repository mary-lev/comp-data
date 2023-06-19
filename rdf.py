import json
import pandas as pd
from typing import List
from rdflib import RDF, Literal, URIRef, Graph
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.namespace import RDFS
from sparql_dataframe import get as get_sparql
from pymantic import sparql

from processor import Processor, QueryProcessor


class CollectionProcessor(Processor):

    def uploadData(self, filename: str) -> bool:
        collection = URIRef("http://iiif.io/api/presentation/3#Collection")
        manifest = URIRef("http://iiif.io/api/presentation/3#Manifest")
        canvas = URIRef("http://iiif.io/api/presentation/3#Canvas")
        has_item = URIRef("http://iiif.io/api/presentation/3#hasItem")

        my_graph = Graph()

        with open(filename, "r") as user_file:
            json_file = json.load(user_file)

            for key, value in json_file.items():
                collection_subject = URIRef(json_file["id"])
                if key == "type" and value == "Collection":
                    type_triple = (collection_subject, RDF.type, collection)
                    my_graph.add(type_triple)
                    label = Literal(json_file["label"]["none"][0])
                    label_triple = (collection_subject, RDFS.label, label)
                    my_graph.add(label_triple)

                    for item in json_file["items"]:
                        if item["type"] == "Manifest":
                            manifest_subject = URIRef(item["id"])
                            type_triple = (manifest_subject, RDF.type, manifest)
                            my_graph.add(type_triple)
                            label = Literal(item["label"]["none"][0])
                            label_triple = (manifest_subject, RDFS.label, label)
                            my_graph.add(label_triple)
                            triple = (collection_subject, has_item, manifest_subject)
                            my_graph.add(triple)

                            for each in item["items"]:
                                if each["type"] == "Canvas":
                                    canvas_subject = URIRef(each["id"])
                                    type_triple = (canvas_subject, RDF.type, canvas)
                                    my_graph.add(type_triple)
                                    label = Literal(each["label"]["none"][0])
                                    label_triple = (canvas_subject, RDFS.label, label)
                                    my_graph.add(label_triple)
                                    triple = (manifest_subject, has_item, canvas_subject)
                                    my_graph.add(triple)

            store = SPARQLUpdateStore()
            store.open((self.dbPathOrUrl, self.dbPathOrUrl))
            for triple in my_graph.triples((None, None, None)):
                store.add(triple)
            store.close()
        return True


class TriplestoreQueryProcessor(QueryProcessor):
    prefix_sc = "PREFIX sc: <http://iiif.io/api/presentation/3#> "

    def getEntityById(self, id: str) -> pd.DataFrame:
        query = f"""select ?id ?type ?label
            WHERE {{
                BIND(<{id}> AS ?id)
            ?id rdf:type ?type ;
            rdfs:label ?label .
            }}"""
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql

    def getAllCanvases(self):
        """it returns a data frame containing all the canvases included in the database."""

        query = self.prefix_sc  + """select ?id ?label ?title where
            {
                ?manifest sc:hasItem ?id .
                ?id rdfs:label ?label .
                ?id rdf:type sc:Canvas .
                ?manifest rdfs:label ?title .
            }
        """
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql

    def getAllCollections(self):
        """it returns a data frame containing all the collections included in the database."""

        query = self.prefix_sc + "select ?id ?label where { ?id ?p sc:Collection . ?id rdfs:label ?label . }"
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql

    def getAllManifests(self):
        """it returns a data frame containing all the manifests included in the database."""

        query = self.prefix_sc + """select ?id ?label where
            {
                ?id ?p sc:Manifest .
                ?id rdfs:label ?label .
            }
        """
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql

    def getCanvasesInCollection(self, collection_id: str):
        """it returns a data frame containing all the canvases included in the database
        that are contained in the collection identified by the input identifier.
        Example:
        PREFIX sc: <http://iiif.io/api/presentation/3#>
        select * where {
            <https://dl.ficlit.unibo.it/iiif/28429/collection> sc:hasItem ?manifest .
            ?manifest sc:hasItem ?canvas .
          ?canvas rdfs:label ?label .
          ?canvas rdf:type ?type .
          ?manifest rdfs:label ?title .
        }
        """

        query = self.prefix_sc + "select * where { <" + collection_id + "> sc:hasItem ?manifest . ?manifest sc:hasItem ?id . ?id rdfs:label ?label . ?id rdf:type ?type . ?manifest rdfs:label ?title .}"
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql

    def getCanvasesInManifest(self, manifest_id: str):
        """it returns a data frame containing all the canvases included in the database
        that are contained in the manifest identified by the input identifier.
        Example:
        PREFIX sc: <http://iiif.io/api/presentation/3#>
        select ?s where { <https://dl.ficlit.unibo.it/iiif/2/28429/manifest> sc:hasItem ?s . }
        """

        query = self.prefix_sc + "select ?id ?label ?title where { <" + manifest_id + "> sc:hasItem ?id . ?id rdfs:label ?label . <" + manifest_id + "> rdfs:label ?title . }"
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql

    def getManifestsInCollection(self, collection_id: str):
        """it returns a data frame containing all the manifests included in the database
        that are contained in the collection identified by the input identifier."""

        query = self.prefix_sc + "select * where { <" + collection_id + "> sc:hasItem ?id . ?id rdfs:label ?label . ?id rdf:type ?type . }"
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql

    def getEntitiesWithLabel(self, label: str):
        """it returns a data frame containing all the entities included in the database
        that have the input label."""

        query = self.prefix_sc + "SELECT * WHERE { ?id rdfs:label '" + label + "' .  ?id rdf:type ?type . ?id rdfs:label ?label . }"""
        df_sparql = get_sparql(self.dbPathOrUrl, query, True)
        return df_sparql
