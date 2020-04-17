from crawlers.crawler import Crawler
from email_sender.subscriber import Subscriber
from email_sender.mail_sender import MailSender

def main():
    Crawler().run()
    subscriber_list = Subscriber.get_contacts()
    MailSender().send(subscriber_list)

if __name__ == '__main__':
    main()