import csv
import os

class Contact:
    contacts_file_path = os.path.dirname(os.path.abspath(__file__)) + '/contacts.csv'

    def __init__(self, email):
        self.email = email
    
    @staticmethod
    def get_contacts():
        contact_list = []
        
        with open(Contact.contacts_file_path) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                contact_email = row[0]
                contact = Contact(contact_email)
                contact_list.append(contact)

        return contact_list