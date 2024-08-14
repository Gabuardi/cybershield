import psycopg2
from rest_api.adapters.ticket_adapter import tickets_adapter
from rest_api.config_params import MQService
from typing import Tuple


class TicketOperations:

    def __init__(self, db_config: dict, mq_service: MQService):
        self.db_config = db_config
        self.mq = mq_service

    def create_new_ticket(self, ticket_data: dict):
        mq_body = {
            "summary": ticket_data["summary"],
            "description": ticket_data["description"],
            "solution": ticket_data["solution"],
            "priority": ticket_data["priority"],
            "asset_info": {
                "owner_org_name": ticket_data["org"],
                "ip": ticket_data["ip"],
                "dns": ticket_data["dns"],
                "os": ticket_data["os"]
            }
        }
        self.mq.send_mq_message(
            "reports_ms.queue",
            "create_new_report",
            mq_body
        )

    def get_ticket_list_by_asset(self, asset_id_list: Tuple):
        sql = """SELECT to_json(s.*)
                    FROM tickets AS s
                    WHERE asset IN %s"""
        result = []
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (asset_id_list,))
                    rows = cursor.fetchall()
                    if rows:
                        result = rows
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            return error
        finally:
            return tickets_adapter(result)

    def assign_new_user(self, ticket_id: int, user_id: int):
        mq_body = {
            "user_id": user_id,
            "ticket_id": ticket_id
        }
        self.mq.send_mq_message(
            "tickets_ms.queue",
            "assign_new_user",
            mq_body
        )

    def set_new_status(self, ticket_id: int, data: dict):
        mq_body = {
            "new_status_id": data["new_status_id"],
            "ticket_id": ticket_id,
            "current_user_id": data["current_user_id"]
        }
        self.mq.send_mq_message(
            "tickets_ms.queue",
            "update_status",
            mq_body
        )
