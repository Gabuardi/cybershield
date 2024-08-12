import psycopg2
import hashlib


class UsersOperations:

    def __init__(self, db_config: dict):
        self.db_config = db_config

    @staticmethod
    def encrypt_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def insert_new_user(self, user_data: dict):
        sql = """INSERT INTO users(name, last_name, email, password)
                    VALUES(%s, %s, %s, %s)"""
        user_data['password'] = self.encrypt_password(user_data['password'])

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (
                        user_data["name"], user_data["last_name"],
                        user_data["email"], user_data["password"]))
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_user_password(self, user_id: int, new_password: str):
        sql = """UPDATE users
                    SET password = %s
                    WHERE user_id = %s"""
        new_encrypted_password = self.encrypt_password(new_password)

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (new_encrypted_password, user_id))
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_new_org(self, org_data: dict):
        sql = """INSERT INTO organizations(org_name)
                    VALUES(%s)"""

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (org_data["name"],))
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def add_user_to_org(self, user_id: int, org_id: int):
        sql = """INSERT INTO users_in_organization(user_id, org_id)
                    VALUES(%s, %s)"""

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (user_id, org_id))
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def remove_user_from_org(self, user_id: int, org_id: int):
        sql = """DELETE FROM users_in_organization
                    WHERE user_id = %s AND org_id = %s"""

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (user_id, org_id))
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
