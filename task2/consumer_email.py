import pika

from models import Model

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


# channel.exchange_declare(exchange='topic_service', exchange_type='topic')
channel.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    pk = body.decode()
    mail = Model.objects(id=pk, boolean=False).first()
    if mail:
        mail.update(set__boolean=True)
        print(f"Email updated {mail.id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)


if __name__ == '__main__':
    channel.start_consuming()
