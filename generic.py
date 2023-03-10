
class GenericQueryProcessor(Processor):
    queryProcessors = []
    """the variable containing the list of QueryProcessor objects to involve when one of the get methods below is executed. 
    In practice, every time a get method is executed, the method will call the related method on 
    all the QueryProcessor objects included in the variable queryProcessors, before combining the results and returning the requested object."""

    def cleanQueryProcessors():
        """It clean the list queryProcessors from all the QueryProcessor objects it includes."""
        pass

    def addQueryProcessor():
        """It append the input QueryProcessor object to the list queryProcessors."""
        pass

    def getAllAnnotations():
        """it returns a list of objects having class Annotation included in the databases accessible via the query processors."""
        pass

    def getAllCanvas():
        """it returns a list of objects having class Canvas included in the databases accessible via the query processors."""
        pass

    def getAllCollections():
        """it returns a list of objects having class Collection included in the databases accessible via the query processors."""
        pass

    def getAllImages():
        """it returns a list of objects having class Image included in the databases accessible via the query processors."""
        pass

    def getAllManifests():
        """it returns a list of objects having class Manifest included in the databases accessible via the query processors."""
        pass

    def getAnnotationsToCanvas():
        """it returns a list of objects having class Annotation, included in the databases 
        accessible via the query processors, that have, as annotation target, the canvas specified by the input identifier."""

    def getAnnotationsToCollection():
        """it returns a list of objects having class Annotation, included in the databases accessible 
        via the query processors, that have, as annotation target, the collection specified by the input identifier."""
        pass

    def getAnnotationsToManifest():
        """it returns a list of objects having class Annotation, included in the databases accessible 
        via the query processors, that have, as annotation target, the manifest specified by the input identifier."""
        pass

    def getAnnotationsWithBody():
        """it returns a list of objects having class Annotation, included in the databases accessible 
        via the query processors, that have, as annotation body, the entity specified by the input identifier."""
        pass

    def getAnnotationsWithBodyAndTarget():
        """it returns a list of objects having class Annotation, included in the databases accessible 
        via the query processors, that have, as annotation body and annotation target, the entities specified by the input identifiers."""
        pass

    def getAnnotationsWithTarget():
        """it returns a list of objects having class Annotation, included in the databases accessible 
        via the query processors, that have, as annotation target, the entity specified by the input identifier."""
        pass

    def getCanvasesInCollection():
        """it returns a list of objects having class Canvas, included in the databases accessible 
        via the query processors, that are contained in the collection identified by the input identifier."""
        pass

    def getCanvasesInManifest():
        """it returns a list of objects having class Canvas, included in the databases accessible 
        via the query processors, that are contained in the manifest identified by the input identifier."""
        pass

    def getEntityById():
        """it returns a object having class Entity identify the entity available in the databases accessible 
        via the query processors matching the input identifier (i.e. maximum one entity)."""
        pass

    def getEntitiesWithCreator():
        """it returns a list of objects having class EntityWithMetadata, included in the databases accessible 
        via the query processors, related to the entities having the input creator as one of their creators."""
        pass

    def getEntitiesWithLabel():
        """it returns a list of objects having class EntityWithMetadata, included in the databases accessible 
        via the query processors, related to the entities having, as label, the input label."""
        pass

    def getEntitiesWithTitle():
        """it returns a list of objects having class EntityWithMetadata, included in the databases accessible 
        via the query processors, related to the entities having, as title, the input title."""
        pass

    def getImagesAnnotatingCanvas():
        """it returns a list of objects having class Image, included in the databases accessible 
        via the query processors, that are body of the annotations targetting the canvaes specified by the input identifier."""
        pass

    def getManifestsInCollection():
        """it returns a list of objects having class Manifest, included in the databases accessible 
        via the query processors, that are contained in the collection identified by the input identifier."""
        pass
