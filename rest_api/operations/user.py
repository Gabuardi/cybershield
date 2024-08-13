from typing import List
from rest_api.adapters.user_adapters import (
    encrypt_password,
    user_in_org_adapter
)
import psycopg2


class UserOperations:

    def __init__(self, db_config: dict):
        self.db_config = db_config

    def authenticate(self, email: str, password: str) -> bool:
        sql = """SELECT password
                FROM users
                WHERE email = %s"""

        result = False
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (email,))
                    row = cursor.fetchone()
                    if row and row[0] == encrypt_password(password):
                        result = True
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            return error
        finally:
            return result

    def get_user_orgs(self, user_id: int) -> List[int]:
        sql = """SELECT row_to_json(s.*)
                FROM users_in_organization AS s
                WHERE user_id = %s"""
        result = []

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (user_id,))
                    rows = cursor.fetchall()
                    if rows:
                        result = rows
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            return error
        finally:
            return user_in_org_adapter(result)

    def get_user_data(self, email: str) -> dict:
        sql = """SELECT to_json(s.*)
                   FROM users AS s
                   WHERE email = %s"""
        result = None
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, ("cr7@futbol.com",))
                    row = cursor.fetchone()
                    if row is not None:
                        result = row[0]
                        id = result["user_id"]
                        result["orgs"] = UserOperations(
                            self.db_config).get_user_orgs(id)
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            return error
        finally:
            return result
