from typing import Tuple
from rest_api.adapters.asset_adapters import asset_by_org_adapter
import psycopg2


class AssetOperation:

    def __init__(self, db_config: dict):
        self.db_config = db_config

    def get_assets_by_org(self, org_list: Tuple):
        sql = """SELECT to_json(s.*)
                FROM assets AS s
                WHERE owner_org IN %s"""
        result = []
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (org_list,))
                    rows = cursor.fetchall()
                    if rows:
                        result = rows
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            return error
        finally:
            return asset_by_org_adapter(result)
