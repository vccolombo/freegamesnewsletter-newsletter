import logging
from scrapy.utils.log import configure_logging

from crawlers.crawler import Crawler
from email_sender.subscriber import Subscriber
from email_sender.mail_sender import MailSender

def main():
    configure_logging(settings={
        'LOG_LEVEL': 'INFO'
    })
    logging.basicConfig(level=logging.INFO)
    
    Crawler().run_newsletter()
    subscriber_list = Subscriber.get_contacts()
    MailSender().send(subscriber_list)

if __name__ == '__main__':
    main()