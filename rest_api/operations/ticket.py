from rest_api.config_params import MQService


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

