#!/usr/bin/env python
import pika

class queue:
    def __init__(self, name):
        self.name = name
        self.connection = None
        self.channel = None
        self.isOpen = False

    def open(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.name)
        self.isOpen = True

    def publish(self, msg):
        if not self.isOpen:
            self.open()
        self.channel.basic_publish(exchange='',
                                   routing_key=self.name,
                                   body=msg)

    def consume(self, callback):
        if not self.isOpen:
            self.open()
        self.channel.basic_consume(callback,
                                   queue=self.name,
                                   no_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
        self.isOpen = False
        self.channel = None
        self.connection = None
