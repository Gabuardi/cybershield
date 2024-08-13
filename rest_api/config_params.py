import os
import json
import pika
from dotenv import load_dotenv


class ConfigParams:

    def __init__(self):
        load_dotenv()

    @property
    def db_params(self):
        return {
            "database": os.getenv("DB_NAME"),
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USERNAME"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT"),
        }

    @property
    def mq_params(self):
        return {
            "host": os.getenv("MQ_HOST"),
            "username": os.getenv("MQ_USERNAME"),
            "password": os.getenv("MQ_PASSWORD"),
        }

class MQService:

    def __init__(self, mq_params: dict):
        credentials = pika.PlainCredentials(
            mq_params["username"],
            mq_params["password"]
        )
        self.connection_params = pika.ConnectionParameters(
            host='localhost',
            credentials=credentials
        )

    @staticmethod
    def set_operation_header(operation: str) -> pika.BasicProperties:
        return pika.BasicProperties(
            headers={
                "operation": operation
            }
        )

    def send_mq_message(self, queue: str, operation: str, body: dict):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.basic_publish(
            routing_key=queue,
            body=json.dumps(body),
            properties=self.set_operation_header(operation)
        )
        connection.close()
