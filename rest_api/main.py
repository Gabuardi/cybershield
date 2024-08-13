from fastapi import FastAPI, Request, HTTPException
from rest_api.config_params import ConfigParams, MQService
from rest_api.operations import (
    UserOperations,
    TicketOperations
)

from rest_api.adapters.user_adapters import get_auth_header

app = FastAPI()
db_config = ConfigParams().db_params

mq_service = MQService(ConfigParams().mq_params)
user_ops = UserOperations(db_config)
ticket_ops = TicketOperations(db_config, mq_service)


# ----------------------------------------------------------------------------
# USER
# ----------------------------------------------------------------------------
@app.get("/login", tags=["User Management"])
def get_user_data(request: Request):
    credentials = get_auth_header(request)
    if user_ops.authenticate(**credentials):
        return user_ops.get_user_data("cr7@futbol.com")
    raise HTTPException(status_code=401, detail="Unauthorized")


@app.put('/password-update/{user_id}', tags=["User Management"])
def update_user_password(user_id: int, body: dict, request: Request):
    credentials = get_auth_header(request)
    if user_ops.authenticate(**credentials):
        mq_body = {
            "user_id": user_id,
            "new_password": body["new_password"]
        }
        mq_service.send_mq_message(
            "users_ms.queue",
            "update_password",
            mq_body
        )
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# ----------------------------------------------------------------------------
# VULNERABILITY REPORT
# ----------------------------------------------------------------------------
@app.post("/report/vulnerability", tags=["Vulnerability Report"])
def report_new_vulnerability(body: dict, request: Request):
    credentials = get_auth_header(request)
    if user_ops.authenticate(**credentials):
        ticket_ops.create_new_ticket(body)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
