import os
from dotenv import load_dotenv


class ConfigParams:

    def __init__(self):
        load_dotenv()

    @property
    def db_params(self):
        return {
            "database": os.getenv("db_name"),
            "host": os.getenv("db_host"),
            "user": os.getenv("db_username"),
            "password": os.getenv("db_password"),
            "port": os.getenv("db_port"),
        }

    @property
    def mq_params(self):
        return {
            "host": os.getenv("MQ_HOST"),
            "username": os.getenv("MQ_USERNAME"),
            "password": os.getenv("MQ_PASSWORD"),
        }
