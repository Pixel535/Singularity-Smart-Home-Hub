import threading

import pika


def init_rabbit():
    def callback(ch, method, properties, body):
        print("Otrzymano:", body.decode())

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="activity_queue")
    channel.basic_consume(queue="activity_queue", on_message_callback=callback, auto_ack=True)

    print("[RabbitMQ] Czekam na wiadomości...")
    channel.start_consuming()


def start_rabbit_thread():
    rabbit_thread = threading.Thread(target=init_rabbit, daemon=True)
    rabbit_thread.start()
    print("[RabbitMQ] Nasłuchiwanie uruchomione w tle.")

