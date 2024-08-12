import json
from typing import Callable

import pika
from tickets_ms.config_params import ConfigParams
from operations import TicketsOperations

config = ConfigParams()
mq_params = config.mq_params
credentials = pika.PlainCredentials(mq_params["username"],
                                    mq_params["password"])
mq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=mq_params["host"], credentials=credentials))
channel = mq_connection.channel()
channel.queue_declare(queue="tickets_ms.queue")
ticket_operations = TicketsOperations(db_config=config.db_params)


def map_operation(operation_name: str) -> Callable:
    try:
        return {
            "assign_new_user": ticket_operations.update_assignee,
            "update_status": ticket_operations.update_status
        }[operation_name]
    except KeyError:
        print("ERROR: Invalid operation")


def handle_request(ch, method, properties, body):
    print("------------------------------------------------------------------")
    operation_name = properties.headers["operation"]
    operation = map_operation(operation_name)
    request_body = json.loads(body)
    print(f"==> Request received :=> {operation_name}")
    if operation is not None:
        operation(request_body)


def run_microservice():
    print(
        '==> Listening message queue, waiting for logs. To exit press CTRL+C')
    channel.basic_consume(queue="tickets_ms.queue",
                          on_message_callback=handle_request,
                          auto_ack=True)
    channel.start_consuming()


run_microservice()
