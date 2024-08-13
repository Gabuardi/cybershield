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
            org_id = self.org_lookup(data['owner_org_name'])
            if org_id is not None:
                with psycopg2.connect(**self.db_config) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql, (
                            org_id,
                            data["ip"],
                            data["dns"],
                            data["os"]))
                        row = cursor.fetchone()
                        if row is not None:
                            created_asset_id = row[0]
                            print(
                                f'==> New asset created successfully with ID: {created_asset_id}')
                        conn.commit()
            else:
                print(
                    f"ERROR: organization {data['owner_org_name']} does not exist")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return created_asset_id

    def asset_lookup(self, ip: str) -> int:
        sql = """SELECT asset_id
                        FROM assets
                        WHERE ip = %s"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (ip,))
                    row = cursor.fetchone()
                    if row is not None:
                        return row[0]
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_asset_id(self, asset_data: dict) -> int:
        asset_id_lookup = self.asset_lookup(asset_data["ip"])

        if asset_id_lookup is not None:
            return asset_id_lookup
        else:
            return self.create_new_asset(asset_data)

    def new_report(self, data: dict):
        asset_id = self.get_asset_id(data["asset_info"])
        if asset_id is not None:
            sql = """INSERT INTO tickets (asset, status, summary, description, solution, priority)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
            try:
                with psycopg2.connect(**self.db_config) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql, (
                            asset_id,
                            1,
                            data["summary"],
                            data["description"],
                            data["solution"],
                            data["priority"]
                        ))

                        row = cursor.fetchone()
                        if row is not None:
                            created_id = row[0]
                            print(
                                f'==> New vulnerability ticket created successfully with ID: {created_id}')
                            conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        else:
            print(
                "ERROR: Report could not be created, try again with new data")
