import logging
import pika
import json
import os

class EmailBroker:
    RABBITMQ_USER = os.environ["RABBITMQ_USER"]
    RABBITMQ_PASS = os.environ["RABBITMQ_PASS"]
    QUEUE = "emails"

    logger = logging.getLogger(__name__)

    def __init__(self):
        credentials = pika.PlainCredentials(
            self.RABBITMQ_USER, self.RABBITMQ_PASS)
        self._params = pika.ConnectionParameters(
            "rabbitmq", 5672, '/', credentials)
        self._conn = None
        self._channel = None

    def connect(self):
        if not self._conn or self._conn.is_closed:
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()
            self._channel.queue_declare(queue=self.QUEUE, durable=True)

    def close(self):
        if self._conn and self._conn.is_open:
            self.logger.info('closing queue connection')
            self._conn.close()

    def publish_email(self, receiver_email, subject, html):
        try:
            msg = {
                "email": receiver_email,
                "subject": subject,
                "html": html
            }
            self._channel.basic_publish(
                exchange='', routing_key=self.QUEUE, body=json.dumps(msg))
        except pika.exceptions.ConnectionClosed:
            self.logger.warn("Reconnecting to queue")
            self.connect()
            self._channel.basic_publish(
                exchange='', routing_key=self.QUEUE, body=json.dumps(msg))