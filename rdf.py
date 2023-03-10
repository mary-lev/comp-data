# all the classes for handling RDF database
from processor import Processor


class CollectionProcessor(Processor):

    def uploadData():
        """it takes in input the path of a JSON file containing collections (with manifests and canvases) 
        and uploads them in the database. This method can be called everytime there is a need to upload collections in the database."""
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

