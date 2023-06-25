# all the classes for handling the relational database
# AnnotationProcessor, MetadataProcessor, RelationalQueryProcessor

import csv
import sqlite3
import pandas as pd
from processor import Processor, QueryProcessor


all = [
    "AnnotationProcessor",
    "MetadataProcessor",
    "QueryProcessor",
    "RelationalQueryProcessor",
]


class AnnotationProcessor(Processor):

    def uploadData(self, filename: str) -> bool:
        """it takes in input the path of a CSV file containing annotations and uploads them in the database.
        This method can be called everytime there is a need to upload annotations in the database."""
        connection = sqlite3.connect(self.dbPathOrUrl)
        cursor = connection.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS annotations(
                id STRING PRIMARY KEY,
                body STRING NOT NULL,
                target STRING NOT NULL,
                motivation STRING NOT NULL);
                '''
        cursor.execute(create_table)
        with open(filename, "r", encoding="utf-8") as file:
            contents = csv.reader(file)
            next(contents)
            insert_records = "INSERT INTO annotations (id, body, target, motivation) VALUES(?, ?, ?, ?)"
            try:
                cursor.executemany(insert_records, contents)
                connection.commit()
                connection.close()
            except sqlite3.IntegrityError:
                print("Error: the database already contains the entity with the same identifier.")
        return True


class MetadataProcessor(Processor):

    def uploadData(self, filename: str) -> bool:
        """it takes in input the path of a CSV file containing metadata and uploads them in the database.
        This method can be called everytime there is a need to upload metadata in the database."""

        connection = sqlite3.connect(self.dbPathOrUrl)
        cursor = connection.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS metadata(
                id STRING PRIMARY KEY,
                title STRING NOT NULL,
                creator STRING NOT NULL);
                '''
        cursor.execute(create_table)
        with open(filename, "r", encoding="utf-8") as file:
            contents = csv.reader(file)
            next(contents)
            insert_records = "INSERT INTO metadata (id, title, creator) VALUES(?, ?, ?)"
            try:
                cursor.executemany(insert_records, contents)
                connection.commit()
                connection.close()
            except sqlite3.IntegrityError:
                print("Error: the database already contains the entity with the same identifier.")
        return True


class RelationalQueryProcessor(QueryProcessor):

    def getEntityById(self, id: str) -> pd.DataFrame:
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT * FROM metadata WHERE id = ?"
            result = pd.read_sql(query, con, params=(id,))
            if not result.empty:
                return result
            query = "SELECT * FROM annotations WHERE id = ?"
            result = pd.read_sql(query, con, params=(id,))
            return result

    def getAllAnnotations(self):
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT * FROM annotations"
            df_sql = pd.read_sql(query, con)
        return df_sql

    def getAllImages(self):
        """it returns a data frame containing all the images included in the database."""
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT body FROM annotations"
            df_sql = pd.read_sql(query, con)
        return df_sql

    def getAnnotationsWithBody(self, body):
        """"it returns a data frame containing all the annotations included in the database
        that have, as annotation body, the entity specified by the input identifier."""
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT * FROM annotations"
            df_sql = pd.read_sql(query, con)

        return df_sql.query(f"body == '{body}'")

    def getAnnotationsWithTarget(self, target):
        """it returns a data frame containing all the annotations included in the database
        that have, as annotation target, the entity specified by the input identifier."""
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT * FROM annotations"
            df_sql = pd.read_sql(query, con)
        return df_sql.query(f"target == '{target}'")

    def getAnnotationsWithBodyAndTarget(self, body, target):
        """it returns a data frame containing all the annotations included in the database
        that have, as annotation body and annotation target, the entities specified by the input identifiers."""
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT * FROM annotations"
            df_sql = pd.read_sql(query, con)
        return df_sql.query(f"body == '{body}' and target == '{target}'")

    def getEntitiesWithCreator(self, creator):
        """it returns a data frame containing all the metadata included in the database
        related to the entities having the input creator as one of their creators."""
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT * FROM metadata"
            df_sql = pd.read_sql(query, con)
        print("With creator: ", df_sql[df_sql['creator'].str.contains(creator)])
        return df_sql[df_sql['creator'].str.contains(creator)]

    def getEntitiesWithTitle(self, title):
        """it returns a data frame containing all the metadata included in the database
        related to the entities having, as title, the input title."""
        with sqlite3.connect(self.dbPathOrUrl) as con:
            query = "SELECT * FROM metadata"
            df_sql = pd.read_sql(query, con)
        return df_sql.query(f"title == '{title}'")
