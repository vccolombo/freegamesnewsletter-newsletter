from crawlers.crawler import Crawler
from email_sender.contact import Contact
from email_sender.mail_sender import MailSender

def main():
    Crawler().run()
    contact_list = Contact.get_contacts()
    MailSender().send(contact_list)

if __name__ == '__main__':
    main()