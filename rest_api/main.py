import psycopg2
from fastapi import FastAPI, Request, HTTPException
from config_params import ConfigParams
from operations.user import UserOperations
import base64

app = FastAPI()
db_config = ConfigParams().db_params


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


@app.get("/login", tags=["User Management"])
def get_user_data(request: Request):
    credentials = get_auth_header(request)
    if UserOperations(db_config).authenticate(**credentials):
        return UserOperations(db_config).get_user_data("cr7@futbol.com")
    raise HTTPException(status_code=401, detail="Unauthorized")
