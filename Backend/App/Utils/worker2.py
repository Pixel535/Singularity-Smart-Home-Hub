import pika

def callback(ch, method, properties, body):
    print("Otrzymano:", body.decode())

def init_rabbit():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="activity_queue")
    channel.basic_consume(queue="activity_queue", on_message_callback=callback, auto_ack=True)
    print("Czekam na wiadomości...")
    channel.start_consuming()