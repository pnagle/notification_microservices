#!/usr/bin/env python
import pika
import sys, time
is_pdf = False


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_notifications',
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='direct_notifications',
                   queue=queue_name,
                   routing_key='email')

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    queue_name_pdf = body.split(" : ")
    print(" [x] Requesting PDF status")

    channel.queue_declare(queue=queue_name_pdf[1])

    def callback(ch, method, properties, body):
        global is_pdf
        if body == 'PDF':
            is_pdf = True
            print ("Email sent with pdf generated")
        else:
            is_pdf = False
            print ("Email sent invoice will be sent shortly")
        print(" [x] Received %r" % body)
    channel.basic_consume(callback,
                          queue=queue_name_pdf[1],
                          no_ack=True)
    # time.sleep(30)
    # global is_pdf
    # if is_pdf == True:
    #     print ("Email sent with pdf generated")
    #     is_pdf = False
    # else:
    #     print ("Email sent invoice will be sent shortly")


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
