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
    
    def insert_or_update_one(self, table, data, update_key=None):
        if self.db is None:
            logging.error(f"COULDN'T INSERT {data}: db is not initialized")
            return
        
        try:
            collection = self.db[table]
            if update_key:
                key = {update_key: data[update_key]}
                self._update_one(key, data, collection)
            else:
                self._insert_one(data, collection)
        except errors.PyMongoError as err:
            logging.error(f"COULDN'T INSERT {data}: " + err)
    
    def _update_one(self, key, data, collection):
        data = {'$set': data}
        collection.update_one(key, data, upsert=True)

    def _insert_one(self, data, collection):
        collection.insert_one(data)

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