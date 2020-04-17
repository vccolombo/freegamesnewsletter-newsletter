import csv
import os

from data.database import Database

class Subscriber:
    DATABASE_NAME = "freegamesnewsletter"
    TABLE_NAME = "subscribers"

    def __init__(self, email, unsubscribe_code):
        self.email = email
        self.unsubscribe_code = unsubscribe_code

    @staticmethod
    def get_contacts():
        query = Database(Subscriber.DATABASE_NAME).select_all(Subscriber.TABLE_NAME)
        return [Subscriber(row['email'], row['unsubscribeCode']) for row in query]