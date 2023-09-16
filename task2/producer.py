from random import choice

import pika
from faker import Faker

from models import Model


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='topic_service', exchange_type='topic')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='topic_service', queue='email_queue')
channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_bind(exchange='topic_service', queue='sms_queue')


def main():
    r_keys = ['sms', 'email']
    for i in range(10):
        mail = Model(fullname=Faker().name(),
                     email=Faker().ascii_free_email(),
                     phone=Faker().phone_number(),
                     routing_key=choice(r_keys)).save()
        r_key = mail.objects.routing_key()
        routing_key = r_key

        channel.basic_publish(
            exchange='topic_service',
            routing_key=routing_key,
            body=str(mail.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    connection.close()


if __name__ == '__main__':
    main()
