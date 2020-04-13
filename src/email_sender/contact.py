import csv
import os

from data.database import Database

class Contact:
    DATABASE_NAME = "freegamesnewsletter"
    TABLE_NAME = "contacts"

    def __init__(self, email):
        self.email = email
    
    def insert_in_db(self):
        insert_value = {
            'email': self.email
        }
        Database(Contact.DATABASE_NAME).insert_one(self.TABLE_NAME, insert_value)

    @staticmethod
    def get_contacts():
        query = Database(Contact.DATABASE_NAME).select_all(Contact.TABLE_NAME)
        return [Contact(row['email']) for row in query]