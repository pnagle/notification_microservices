#!/usr/bin/env python
import pika
import sys
import uuid


class GeneratePDFRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id=self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

generatepdf_rpc = GeneratePDFRpcClient()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_notifications',
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='direct_notifications',
                   queue=queue_name,
                   routing_key='pdf')

print(' [*] Waiting for pdf . To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    # pdf_generation(body)

    channel.queue_declare(queue=body)

    channel.basic_publish(exchange='',
                          routing_key=body,
                          body='NOPDF')
    print(" [x] Requesting PDF")
    response = generatepdf_rpc.call(30)
    channel.basic_publish(exchange='',
                          routing_key=body,
                          body='PDF')

    print(" [.] Got %r" % response)


channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()



