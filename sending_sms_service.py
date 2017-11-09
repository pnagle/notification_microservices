#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_notifications',
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='direct_notifications',
                   queue=queue_name,
                   routing_key='sms')

print(' [*] Waiting for sms no. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] SMS sent via %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
