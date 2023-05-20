import uuid
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request, Response
from .routers import auth
from fastapi.middleware.cors import CORSMiddleware
import datetime
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse
from app import constants as const
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.log_config import init_loggers
from fastapi.responses import FileResponse
import os
import contextvars
from starlette.datastructures import Headers
import requests
from .config import settings




favicon_path = os.path.join(os.path.dirname(__file__), 'assets', 'favicon.ico')
log = init_loggers(logger_name="main-logger")
# log.info("devent")

app = FastAPI(
    title= const.FASTAPI_METADATA_TITLE,
    version= const.FASTAPI_METADATA_VERSION,
    description= const.FASTAPI_METADATA_DESCRIPTION,
    contact= {
        "name": f"{const.FASTAPI_METADATA_CONTACT_NAME}",
        "url": "https://www.linkedin.com/in/yoad-duani/",
    },
)


print("test")
request_id_contextvar = contextvars.ContextVar("request_id", default=None)


app.add_middleware(
    CORSMiddleware,
    # allow_origins= const.ALLOW_ORIGINS,
    allow_origins= ["*"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers=["*"],
)

# Define a middleware to generate a unique ID for each request
@app.middleware("http")
async def log_request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_contextvar.set(request_id)
    try:
        request.state.request_id = request_id
    except Exception as ex:
        log.error(f"Request failed 1: {ex}", extra={"request_id": request_id})
        try:
            request_id = request.headers.get("X-Request-ID")
        except Exception as ex:
            log.error(f"Request failed 2: {ex}", extra={"request_id": request_id})
        return Response(content="Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    log.extra = {"request_id": request_id}
    try:
        response = await call_next(request)
    except Exception as ex:
        log.error(f"Request failed 3: {ex}", extra={"request_id": request_id})
        try:
            error_response = Response(content=ex, status_code=ex.status_code)
        except Exception as ex:
            error_response = Response(content=ex, status_code=503)
            return error_response
        return error_response
        # response = JSONResponse(content={"success": False}, status_code=500)
    finally:
        try:
            response.headers["X-Request-ID"] = request_id
        except:
            pass
    return response

# @app.middleware("http")
# async def apply_middleware(request: Request, call_next):
#     response = await log_request_id_middleware(request, call_next)
#     return response


app.include_router(auth.router)
# app.include_router(user.router)



# @app.on_event("shutdown")
# def shutdown_event():
#     log.info("devent")
    
@app.get("/")
async def root(request: Request):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
    return {
        "API Name": "Social Network fastAPI bff_server",
        "API Documentation": f"{request.url._url}docs",
        "GitHub Repo": "https://github.com/Yoad-Duani/social_network_fastAPI",
        "Client-IP": f"{request.client.host}",
        "Date": F"{now}"
    }


@app.get("/test-auth")
async def root(request: Request):
    log.info(f"/sent request to auth service", extra={"request_id": request.state.request_id})
    headers = {'X-Request-ID': request.state.request_id}   
    response = requests.get(f'http://{settings.auth_service_url}:{settings.auth_service_port}/test',headers= headers)
    print("this is back in BFF") 
    print(f"{response.json()}")
    return response.json()


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(path=favicon_path, filename=favicon_path)



class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


if __name__ == "__main__":
    uvicorn.run(app)