import hashlib


def encrypt_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def user_in_org_adapter(data: list) -> list[int]:
    result = []
    for row in data:
        for nested in row:
            result.append(nested["org_id"])
    return result
