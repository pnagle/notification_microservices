from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import pika, sys

# Create your models here.


class Order(models.Model):
    """
    Sample order table to collect the orders from post request, attaching direct fields
    instead of the foreign key relations.
    """

    order_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    user = models.CharField(max_length=400)
    phone = models.IntegerField()
    email = models.EmailField()


@receiver(post_save, sender=Order)
def send_email_celery(sender, instance=None, created=False, **kwargs):
    name = instance.user
    email = instance.email
    if created:
        # tasks.send_email.apply_async((instance.email, f_name), countdown=6)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Can use different ip or port for rabbitmq server/image
        channel = connection.channel()
        channel.exchange_declare(exchange='direct_notifications',
                                 exchange_type='direct')

        tasks = ['sms', 'email', 'pdf']

        # Using a direct exchange type
        for each_task in tasks:
            if each_task == 'sms':
                message = instance.phone
            elif each_task == 'email':
                message = email + ' : ' + name + ' - ' + str(instance.order_id)
            elif each_task == 'pdf':
                # pdf_generation(name, instance.order_id)
                message = name + ' - ' + str(instance.order_id)
            channel.basic_publish(exchange='direct_notifications',
                                  routing_key=each_task,
                                  body=str(message))
            print(" [x] Sent %r:%r" % (each_task, message))
        connection.close()
