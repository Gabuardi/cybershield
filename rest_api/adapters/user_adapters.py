import base64
import hashlib
from fastapi import Request


def encrypt_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def user_in_org_adapter(data: list) -> list[int]:
    result = []
    for row in data:
        for nested in row:
            result.append(nested["org_id"])
    return result


def get_auth_header(request: Request):
    header = request.headers.get("Authorization")
    get_auth_credentials = header.split(" ")[1]
    decoded_credentials = base64.b64decode(get_auth_credentials).decode(
        "utf-8")
    credentials = decoded_credentials.split(":")
    return {
        "email": credentials[0],
        "password": credentials[1]
    }