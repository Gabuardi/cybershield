import psycopg2


class ReportsOperations:

    def __init__(self, db_config: dict):
        self.db_config = db_config

    def org_lookup(self, org_name: str) -> int:
        sql = """SELECT org_id
                FROM organizations
                WHERE org_name = %s"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (org_name,))
                    row = cursor.fetchone()
                    if row is not None:
                        return row[0]
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_new_asset(self, data: dict) -> int:
        sql = """INSERT INTO assets (owner_org, ip, dns, os)
                VALUES (%s, %s, %s, %s)
                RETURNING asset_id"""
        created_asset_id = None

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (
                        data["owner_org"],
                        data["ip"],
                        data["dns"],
                        data["os"]))
                    row = cursor.fetchone()
                    if row is not None:
                        created_asset_id = row[0]
                        print(
                            f'==> New asset created successfully with ID: {created_asset_id}')
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return created_asset_id
