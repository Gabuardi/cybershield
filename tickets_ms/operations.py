import psycopg2


class TicketsOperations:

    def __init__(self, db_config: dict):
        self.db_config = db_config

    def update_assignee(self, data: dict):
        sql = """UPDATE tickets
                    SET assignee_user = %s
                    WHERE ticket_id = %s"""

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (
                        data["user_id"],
                        data["ticket_id"],))
                    conn.commit()
                    print(
                        f"==> User #{data['user_id']} assign ticket #{data['ticket_id']} successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_status(self, data: dict):
        sql = """UPDATE tickets
                    SET status = %s
                    WHERE ticket_id = %s"""
        sql2 = """INSERT INTO ticket_logs (ticket_id, new_status_id, user_id)
                    VALUES (%s, %s, %s)"""

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (
                        data["new_status_id"],
                        data["ticket_id"],))
                    conn.commit()
                    print(
                        f"==> Status update ticket #{data['ticket_id']} successfully")
                with conn.cursor() as cursor:
                    cursor.execute(sql2, (
                        data["ticket_id"],
                        data["new_status_id"],
                        data["current_user_id"]))
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_priority(self, data: dict):
        sql = """UPDATE tickets
                       SET priority = %s
                       WHERE ticket_id = %s"""

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (
                        data["new_priority"],
                        data["ticket_id"],))
                    conn.commit()
                    print(
                        f"==> Priority was set to {data['new_priority']} on ticket #{data['ticket_id']}")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
