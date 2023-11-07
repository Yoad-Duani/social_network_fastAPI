from .config import settings
from functools import lru_cache
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, Body, Request
from app.log_config import init_loggers
import httpx
import traceback


@lru_cache()
def get_settings():
    return settings()

AUTH_SERVICE = f"http://{settings.auth_service_url}:{settings.auth_service_port}"
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth')
log = init_loggers(logger_name="oauth2-logger")

async def get_current_user(request: Request, 
                     response: Response, 
                     token: str = Depends(oauth2_schema),
):
    print(token)
    request_id = request.state.request_id
    try:
        log.debug(f"Try auth user", extra={"request_id": request_id})
        headers = {'X-Request-ID': request_id, 'Authorization': f"Bearer {token}"}
        # data = {
        #     "token": token,
        # }
        # , params=data
        request = httpx.Request(method="GET", url=f"{AUTH_SERVICE}/auth/get_current_user", headers=headers)
        async with httpx.AsyncClient() as client:
            response_auth = await client.send(request)
    except:
        log.error(f"An error occurred while try to connect to auth service: {traceback.format_exc()} ", extra={"request_id": request_id})
    res = response_auth.json()
    print(res)
    