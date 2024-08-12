import pika
from config_params import ConfigParams

config = ConfigParams()
mq_params = config.mq_params

credentials = pika.PlainCredentials(mq_params["username"], mq_params["password"])
mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_params["host"], credentials=credentials))
channel = mq_connection.channel()
channel.queue_declare(queue='users_ms.queue')


def callback(ch, method, properties, body):
    print(properties)
    print(f"Received {body}")


print('==> Listening message queue, waiting for logs. To exit press CTRL+C')
channel.basic_consume(queue="users_ms.queue", on_message_callback=callback, auto_ack=True)
channel.start_consuming()
