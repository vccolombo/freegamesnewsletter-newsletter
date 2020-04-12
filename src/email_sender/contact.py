import csv

class Contact:
    def __init__(self, email):
        self.email = email
    
    @staticmethod
    def get_contact_list():
        contacts_file_path = 'contacts.csv'
        contact_list = []
        
        with open(contacts_file_path) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                contact_email = row[0]
                contact = Contact(contact_email)
                contact_list.append(contact)

        return contact_list