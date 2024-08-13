from fastapi import FastAPI, Request, HTTPException
from rest_api.config_params import ConfigParams
from rest_api.operations.user import UserOperations

from rest_api.adapters.user_adapters import get_auth_header

app = FastAPI()
db_config = ConfigParams().db_params

user_ops = UserOperations(db_config)


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
    print(user_id)
    print(body)
