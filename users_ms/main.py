from json import JSONDecodeError
from typing import Callable
import pika
from config_params import ConfigParams
from operations import UsersOperations
import json

config = ConfigParams()
mq_params = config.mq_params

credentials = pika.PlainCredentials(mq_params["username"],
                                    mq_params["password"])
mq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=mq_params["host"], credentials=credentials))
channel = mq_connection.channel()
channel.queue_declare(queue='users_ms.queue')
user_operations = UsersOperations(config.db_params)


def map_operation(operation_name: str) -> Callable:
    try:
        return {
            "create_user": user_operations.insert_new_user,
            "update_password": user_operations.update_user_password,
            "create_organization": user_operations.insert_new_org,
            "add_user_to_organization": user_operations.add_user_to_org,
            "remove_user_from_organization": user_operations.remove_user_from_org
        }[operation_name]
    except KeyError:
        print("ERROR: Invalid operation")


def handle_request(ch, method, properties, body):
    try:
        print(
            "------------------------------------------------------------------")
        operation_name = properties.headers["operation"]
        operation = map_operation(operation_name)
        request_body = json.loads(body)
        print(f"==> Request received :=> {operation_name}")
        if operation is not None:
            operation(request_body)
    except JSONDecodeError:
        print("ERROR: Invalid JSON")


def run_microservice():
    print(
        '==> Listening message queue, waiting for logs. To exit press CTRL+C')
    channel.basic_consume(queue="users_ms.queue",
                          on_message_callback=handle_request,
                          auto_ack=True)
    channel.start_consuming()


run_microservice()
