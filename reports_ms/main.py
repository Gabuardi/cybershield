import json
from json import JSONDecodeError
from typing import Callable

import pika
from tickets_ms.config_params import ConfigParams
from operations import ReportsOperations

config = ConfigParams()
mq_params = config.mq_params
QUEUE_NAME = "reports_ms.queue"
credentials = pika.PlainCredentials(mq_params["username"],
                                    mq_params["password"])
mq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=mq_params["host"], credentials=credentials))
channel = mq_connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
report_operations = ReportsOperations(db_config=config.db_params)


def map_operation(operation_name: str) -> Callable:
    try:
        return {
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
        print("ERROR: Invalid request body")


def run_microservice():
    # print(
    #     '==> Listening message queue, waiting for logs. To exit press CTRL+C')
    # channel.basic_consume(queue=QUEUE_NAME,
    #                       on_message_callback=handle_request,
    #                       auto_ack=True)
    # channel.start_consuming()
    data = {
        "owner_org": 3,
        "ip": "127.0.2.1",
        "dns": "test.cr.2",
        "os": "linux"
    }
    print(report_operations.org_lookup('team_bab2y'))


run_microservice()
