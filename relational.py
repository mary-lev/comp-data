# all the classes for handling the relational database
# AnnotationProcessor, MetadataProcessor, RelationalQueryProcessor

import csv
import sqlite3
from processor import Processor

all = [
    "AnnotationProcessor",
    "MetadataProcessor",
    "QueryProcessor",
    "RelationalQueryProcessor",
]

class AnnotationProcessor(Processor):

    def uploadData(self):
        """it takes in input the path of a CSV file containing annotations and uploads them in the database. 
        This method can be called everytime there is a need to upload annotations in the database."""
        connection = sqlite3.connect(self.dbPathOrUrl)
        cursor = connection.cursor()
        create_table = '''CREATE TABLE annotations(
                id STRING PRIMARY KEY,
                body STRING NOT NULL,
                target STRING NOT NULL,
                motivation STRING NOT NULL);
                '''
        cursor.execute(create_table)
        with open("data/annotations.csv", "r", encoding="utf-8") as file:
            contents = csv.reader(file)
            insert_records = "INSERT INTO annotations (id, body, target, motivation) VALUES(?, ?, ?, ?)"
            cursor.executemany(insert_records, contents)
            select_all = "SELECT * FROM annotations"
            rows = cursor.execute(select_all).fetchall()
            for r in rows:
                print(r)
            connection.commit()
            connection.close()

ap = AnnotationProcessor(path_url="relational.db")
ap.uploadData()


class MetadataProcessor(Processor):

    def uploadData():
        """it takes in input the path of a CSV file containing metadata and uploads them in the database. 
        This method can be called everytime there is a need to upload annotations in the database."""
        pass

 
class QueryProcessor(Processor):

    def getEntityById():
        """it returns a data frame with all the entities matching the input identifier (i.e. maximum one entity)."""


class RelationalQueryProcessor(QueryProcessor):

    def getAllAnnotations():
        """it returns a data frame containing all the annotations included in the database."""
        pass

    def getAllImages():
        """it returns a data frame containing all the images included in the database."""
        pass

    def getAnnotationsWithBody():
        """it returns a data frame containing all the annotations included in the database 
        that have, as annotation body, the entity specified by the input identifier."""
        pass

    def getAnnotationsWithBodyAndTarget():
        """it returns a data frame containing all the annotations included in the database 
        that have, as annotation body and annotation target, the entities specified by the input identifiers."""
        pass

    def getAnnotationsWithTarget():
        """it returns a data frame containing all the annotations included in the database 
        that have, as annotation target, the entity specified by the input identifier."""
        pass

    def getEntitiesWithCreator():
        """it returns a data frame containing all the metadata included in the database 
        related to the entities having the input creator as one of their creators."""
        pass

    def getEntitiesWithLabel():
        """it returns a data frame containing all the metadata included in the database 
        related to the entities having, as label, the input label."""
        pass

    def getEntitiesWithTitle():
        """it returns a data frame containing all the metadata included in the database 
        related to the entities having, as title, the input title."""
        pass