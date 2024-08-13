import os
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
