# all the classes for handling the relational database
# AnnotationProcessor, MetadataProcessor, RelationalQueryProcessor

import csv
import sqlite3
from processor import Processor
from pandas import read_csv
from sqlite3 import connect
from pandas import read_sql

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


class MetadataProcessor(Processor):

    def uploadData(self):
        """it takes in input the path of a CSV file containing metadata and uploads them in the database. 
        This method can be called everytime there is a need to upload metadata in the database."""
        connection = sqlite3.connect(self.dbPathOrUrl)
        cursor = connection.cursor()
        create_table = '''CREATE TABLE metadata(
                id STRING PRIMARY KEY,
                title STRING NOT NULL,
                creator STRING NOT NULL;
                '''
        cursor.execute(create_table)
        with open("data/metadata.csv", "r", encoding="utf-8") as file:
            contents = csv.reader(file)
            insert_records = "INSERT INTO metadata (id, title, creator) VALUES(?, ?, ?)"
            cursor.executemany(insert_records, contents)
            select_all = "SELECT * FROM metadata"
            rows = cursor.execute(select_all).fetchall()
            for r in rows:
                print(r)
            connection.commit()
            connection.close()
        pass

 
class QueryProcessor(Processor):

    def getEntityById():
        """it returns a data frame with all the entities matching the input identifier (i.e. maximum one entity)."""
        with connect("relational.db") as con:
            

class RelationalQueryProcessor(QueryProcessor):
    def getAllAnnotations():
        with connect("relational.db") as con:
            query = "SELECT * FROM annotations"
            df_sql = read_sql(query, con) 
        print(df_sql)
        return df_sql
        

    def getAllImages():
        """it returns a data frame containing all the images included in the database."""
        with connect("relational.db") as con:
            query = "SELECT body FROM annotations"
            df_sql = read_sql(query, con) 
        print(df_sql)
        return df_sql
        
    
        

    def getAnnotationsWithBody(body):
        """"it returns a data frame containing all the annotations included in the database 
        that have, as annotation body, the entity specified by the input identifier."""
        with connect("relational.db") as con:
            query = "SELECT * FROM annotations"
            df_sql = read_sql(query, con) 
            
        return(df_sql.query(f"body == '{body}'"))
        


    def getAnnotationsWithBodyAndTarget(body, target):
        """it returns a data frame containing all the annotations included in the database 
        that have, as annotation body and annotation target, the entities specified by the input identifiers."""
        # df_piblications.query ( "type =='annotations', 'body' and 'target'" )
        with connect("relational.db") as con:
            query = "SELECT * FROM annotations"
            df_sql = read_sql(query, con) 
        return(df_sql.query(f"body == '{body}' and target == '{target}'"))
        


    def getAnnotationsWithTarget(target):
        """it returns a data frame containing all the annotations included in the database 
        that have, as annotation target, the entity specified by the input identifier."""
        with connect("relational.db") as con:
            query = "SELECT * FROM annotations"
            df_sql = read_sql(query, con) 
        return(df_sql.query(f"target == '{target}'"))
                

    def getEntitiesWithCreator(creator):
        """it returns a data frame containing all the metadata included in the database 
        related to the entities having the input creator as one of their creators."""
        with connect("relational.db") as con:
            query = "SELECT * FROM metadata"
            df_sql = read_sql(query, con) 
        return(df_sql.query(f"creator == '{creator}'"))


#это не нужно делать в итоге?
    def getEntitiesWithLabel(): 
        """it returns a data frame containing all the metadata included in the database 
        related to the entities having, as label, the input label."""
        with connect("relational.db") as con:
            query = "SELECT id FROM metadata"
            df_sql = read_sql(query, con) 
        print(df_sql)

    getEntitiesWithLabel()

    def getEntitiesWithTitle(title):
        """it returns a data frame containing all the metadata included in the database 
        related to the entities having, as title, the input title."""
        with connect("relational.db") as con:
            query = "SELECT * FROM metadata"
            df_sql = read_sql(query, con) 
        return(df_sql.query(f"title == '{title}'"))

