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
