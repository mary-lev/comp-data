from typing import List
import pandas as pd
from processor import QueryProcessor
from model import Annotation, Canvas, Collection, Image, Manifest, IdentifiableEntity, EntityWithMetadata


class GenericQueryProcessor(QueryProcessor):
    queryProcessors = []
    """the variable containing the list of QueryProcessor objects to involve when one of the get methods below is executed.
    In practice, every time a get method is executed, the method will call the related method on
    all the QueryProcessor objects included in the variable queryProcessors, before combining the results and returning the requested object."""

    def cleanQueryProcessors(self):
        """It clean the list queryProcessors from all the QueryProcessor objects it includes."""
        self.queryProcessors = []
        return True

    def addQueryProcessor(self, qp) -> bool:
        """It append the input QueryProcessor object to the list queryProcessors."""
        self.queryProcessors.append(qp)
        return True

    def getEntityById(self, id: str):
        for query_processor in self.queryProcessors:
            if "getEntityById" in dir(query_processor):
                data = query_processor.getEntityById(id)
                if not data.empty:
                    return IdentifiableEntity(
                        id=data.to_dict("records")[0]["id"],
                    )
        return None

    def getAllAnnotations(self):
        """it returns a list of objects having class Annotation included in the databases accessible via the query processors."""
        for qp in self.queryProcessors:
            if "getAllAnnotations" in dir(qp):
                annotations = qp.getAllAnnotations()
        if not annotations.empty:
            return [Annotation(
                id=annotation["id"],
                motivation=annotation["motivation"],
                body=Image(id=annotation["body"]),
                target=IdentifiableEntity(id=annotation["target"]),
            ) for _, annotation in annotations.iterrows()]
        return []

    def getAllCanvas(self):
        """it returns a list of objects having class Canvas included in the databases accessible via the query processors."""
        canvases = pd.DataFrame()
        for qp in self.queryProcessors:
            if "getAllCanvases" in dir(qp):
                canvases = qp.getAllCanvases()
                return [Canvas(
                    id=canvas["id"],
                    label=canvas.get("label"),
                    title=canvas.get("title"),
                ) for _, canvas in canvases.iterrows()]

    def getAllImages(self):
        """it returns a list of objects having class Image included in the databases accessible via the query processors."""
        for qp in self.queryProcessors:
            if "getAllImages" in dir(qp):
                images = qp.getAllImages()
                return [Image(
                    id=image["body"],
                ) for _, image in images.iterrows()]

    def getAllManifests(self):
        """it returns a list of objects having class Manifest included in the databases accessible via the query processors."""
        for qp in self.queryProcessors:
            if "getAllManifests" in dir(qp):
                manifests = qp.getAllManifests()
            else:
                relational = qp
        return [Manifest(
            id=manifest["id"],
            label=manifest.get("label"),
            title=relational.getEntityById(manifest["id"]).loc[0, "title"],
            creators=relational.getEntityById(manifest["id"]).loc[0, "creator"],
            list_of_canvas=self.getCanvasesInManifest(manifest["id"]),
        ) for _, manifest in manifests.iterrows()]

    def getAnnotationsToCanvas(self, canvas_id: str):
        """it returns a list of objects having class Annotation, included in the databases
        accessible via the query processors, that have, as annotation target, the canvas specified by the input identifier."""
        for qp in self.queryProcessors:
            if "getAnnotationsWithTarget" in dir(qp):
                annotation = qp.getAnnotationsWithTarget(canvas_id)
                return [Annotation(
                    id=annotation["id"],
                    motivation=annotation["motivation"],
                    body=Image(id=annotation["body"]),
                    target=IdentifiableEntity(id=annotation["target"]),
                ) for _, annotation in annotation.iterrows()]

    def getAnnotationsToCollection(self, collection_id: str):
        """it returns a list of objects having class Annotation, included in the databases accessible
        via the query processors, that have, as annotation target, the collection specified by the input identifier."""
        annotation_data = pd.DataFrame()
        for qp in self.queryProcessors:
            if "getAnnotationsWithTarget" in dir(qp):
                collection = qp.getAnnotationsWithTarget(collection_id)
                annotation_data = pd.concat([annotation_data, collection], ignore_index=True)

        return [Annotation(
            id=annotation["id"],
            motivation=annotation["motivation"],
            body=Image(id=annotation["body"]),
            target=IdentifiableEntity(id=annotation["target"]),
        ) for _, annotation in annotation_data.iterrows()]

    def getAnnotationsToManifest(self, manifest_id: str):
        """it returns a list of objects having class Annotation, included in the databases accessible
        via the query processors, that have, as annotation target, the manifest specified by the input identifier."""
        manifest_data = pd.DataFrame()
        for qp in self.queryProcessors:
            if "getAnnotationsWithTarget" in dir(qp):
                manifest = qp.getAnnotationsWithTarget(manifest_id)
                manifest_data = pd.concat([manifest_data, manifest], ignore_index=True)
        return [Annotation(
            id=annotation["id"],
            motivation=annotation["motivation"],
            body=Image(id=annotation["body"]),
            target=IdentifiableEntity(id=annotation["target"]),
        ) for _, annotation in manifest_data.iterrows()]

    def getAnnotationsWithBody(self, id: str):
        """it returns a list of objects having class Annotation, included in the databases accessible
        via the query processors, that have, as annotation body, the entity specified by the input identifier."""
        for qp in self.queryProcessors:
            if "getAnnotationsWithBody" in dir(qp):
                annotation = qp.getAnnotationsWithBody(id)
                return [Annotation(
                    id=annotation["id"],
                    motivation=annotation["motivation"],
                    body=Image(id=annotation["body"]),
                    target=IdentifiableEntity(id=annotation["target"]),
                ) for _, annotation in annotation.iterrows()]
        return None

    def getAnnotationsWithTarget(self, id: str):
        """it returns a list of objects having class Annotation, included in the databases accessible
        via the query processors, that have, as annotation target, the entity specified by the input identifier."""
        for qp in self.queryProcessors:
            if "getAnnotationsWithTarget" in dir(qp):
                annotation = qp.getAnnotationsWithTarget(id)
                return [Annotation(
                    id=annotation["id"],
                    motivation=annotation["motivation"],
                    body=Image(id=annotation["body"]),
                    target=IdentifiableEntity(id=annotation["target"]),
                ) for _, annotation in annotation.iterrows()]
        return None

    def getAnnotationsWithBodyAndTarget(self, body: str, target: str):
        """it returns a list of objects having class Annotation, included in the databases accessible
        via the query processors, that have, as annotation body and annotation target, the entities specified by the input identifiers."""
        for qp in self.queryProcessors:
            if "getAnnotationsWithBodyAndTarget" in dir(qp):
                annotation = qp.getAnnotationsWithBodyAndTarget(body, target)
                return [Annotation(
                    id=annotation["id"],
                    motivation=annotation["motivation"],
                    body=Image(id=annotation["body"]),
                    target=IdentifiableEntity(id=annotation["target"]),
                ) for _, annotation in annotation.iterrows()]
        return None

    def getCanvasesInCollection(self, collection_id: str):
        """it returns a list of objects having class Canvas, included in the databases accessible
        via the query processors, that are contained in the collection identified by the input identifier."""
        for qp in self.queryProcessors:
            if "getCanvasesInCollection" in dir(qp):
                canvases = qp.getCanvasesInCollection(collection_id)

        return [Canvas(
            id=canvas["id"],
            label=canvas.get("label"),
            title=canvas.get("title"),
        ) for _, canvas in canvases.iterrows()]

    def getCanvasesInManifest(self, manifest_id: str):
        """it returns a list of objects having class Canvas, included in the databases accessible
        via the query processors, that are contained in the manifest identified by the input identifier."""
        for qp in self.queryProcessors:
            if "getCanvasesInManifest" in dir(qp):
                canvases = qp.getCanvasesInManifest(manifest_id)
        return [Canvas(
            id=canvas["id"],
            label=canvas["label"],
            title=canvas["title"],
        ) for _, canvas in canvases.iterrows()]

    def getEntitiesWithCreator(self, creator_id: str):
        """it returns a list of objects having class EntityWithMetadata, included in the databases accessible
        via the query processors, related to the entities having the input creator as one of their creators."""
        for qp in self.queryProcessors:
            if "getEntitiesWithCreator" in dir(qp):
                entities = qp.getEntitiesWithCreator(creator_id)
            else:
                triple_qp = qp
        return [EntityWithMetadata(
            id=entity.get("id"),
            label=triple_qp.getEntityById(entity.get("id")).loc[0, "label"],
            title=entity.get("title"),
            creators=entity.get("creator")
        ) for _, entity in entities.iterrows()]

    def getEntitiesWithLabel(self, label: str):
        """it returns a list of objects having class EntityWithMetadata, included in the databases accessible
        via the query processors, related to the entities having, as label, the input label."""
        for qp in self.queryProcessors:
            if "getEntitiesWithLabel" in dir(qp):
                entities = qp.getEntitiesWithLabel(label)
            else:
                relational_qp = qp

        return [EntityWithMetadata(
            id=entity["id"],
            label=entity["label"],
            title=relational_qp.getEntityById(entity["id"]).loc[0, "title"],
            creators=relational_qp.getEntityById(entity.get("id")).loc[0, "creator"],
        ) for _, entity in entities.iterrows()]

    def getEntitiesWithTitle(self, title: str) -> List[EntityWithMetadata]:
        """it returns a list of objects having class EntityWithMetadata, included in the databases accessible
        via the query processors, related to the entities having, as title, the input title."""
        for qp in self.queryProcessors:
            if "getEntitiesWithTitle" in dir(qp):
                entities = qp.getEntitiesWithTitle(title)
            else:
                triple_qp = qp

        return [EntityWithMetadata(
            id=entity["id"],
            label=triple_qp.getEntityById(entity["id"]).loc[0, "label"],
            title=entity["title"],
            creators=entity["creator"],
        ) for _, entity in entities.iterrows()]

    def getImagesAnnotatingCanvas(self, canvas_id: str):
        """it returns a list of objects having class Image, included in the databases accessible
        via the query processors, that are body of the annotations targetting the canvases specified by the input identifier."""
        for qp in self.queryProcessors:
            if "getAnnotationsWithTarget" in dir(qp):
                canvases = qp.getAnnotationsWithTarget(canvas_id)
                canvases = canvases.to_dict("records")
                return [Image(id=canvas["body"]) for canvas in canvases]

    def getManifestsInCollection(self, collection_id: str):
        """it returns a list of objects having class Manifest, included in the databases accessible
        via the query processors, that are contained in the collection identified by the input identifier."""
        for qp in self.queryProcessors:
            if "getManifestsInCollection" in dir(qp):
                manifests = qp.getManifestsInCollection(collection_id)
            else:
                relational_qp = qp
        return [Manifest(
            id=manifest["id"],
            label=manifest.get("label"),
            title=relational_qp.getEntityById(manifest["id"]).loc[0, "title"],
            creators=relational_qp.getEntityById(manifest["id"]).loc[0, "creator"],
            list_of_canvas=self.getCanvasesInManifest(manifest["id"]),
        ) for _, manifest in manifests.iterrows()]

    def getAllCollections(self):
        """it returns a list of objects having class Collection included in the databases accessible via the query processors."""
        collections = pd.DataFrame()
        for qp in self.queryProcessors:
            if "getAllCollections" in dir(qp):
                collections = qp.getAllCollections()
            else:
                relational_qp = qp
        return [Collection(
            id=collection["id"],
            label=collection.get("label"),
            title=collection.get("title"),
            creators=relational_qp.getEntityById(collection["id"]).to_dict().get("creator", {}).get(0, []),
            list_of_manifests=self.getManifestsInCollection(collection["id"]),
        ) for _, collection in collections.iterrows()]
