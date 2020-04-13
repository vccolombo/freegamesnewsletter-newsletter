import os
from pymongo import MongoClient, errors
import logging

class Database:
    DOMAIN = "localhost"
    PORT = 27017

    db = None

    def __init__(self, database):
        try:
            self.db = MongoClient(self.DOMAIN, self.PORT)[database]
        except errors.ServerSelectionTimeoutError as err:
            logging.error(err)
            return
    
    def insert_one(self, table, data):
        if self.db is None:
            logging.error(f"COULDN'T INSERT {data}: db is not initialized")
            return
        
        try:
            test = self.db[table]
            test.insert_one(data)
        except errors.PyMongoError as err:
            logging.error(f"COULDN'T INSERT {data}: " + err)
    
    def select_all(self, table):
        if self.db is None:
            logging.error(f"COULDN'T SELECT ALL FROM {table}: db is not initialized")
            return []

        try:
            cursor = self.db[table].find()
            return [document for document in cursor]
        except errors.PyMongoError as err:
            logging.error(f"COULDN'T SELECT ALL FROM {table}: " + err)
            return []