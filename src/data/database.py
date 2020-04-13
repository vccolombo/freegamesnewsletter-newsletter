import os
from pymongo import MongoClient, errors

class Database:
    DOMAIN = "localhost"
    PORT = 27017

    db = None

    def __init__(self, database):
        try:
            self.db = MongoClient(self.DOMAIN, self.PORT)[database]
        except errors.ServerSelectionTimeoutError as err:
            # TODO: Log some error
            print(err)
            return
    
    def insert_one(self, table, data):
        if self.db is None:
            # TODO: Log some error
            return
        
        try:
            test = self.db[table]
            test.insert_one(data)
        except errors.PyMongoError as err:
            # TODO: Log some error
            print(err)
    
    def select_all(self, table):
        if self.db is None:
            # TODO: Log some error
            return []

        try:
            cursor = self.db[table].find()
            return [document for document in cursor]
        except errors.PyMongoError as err:
            # TODO: Log some error
            print(err)
            return []