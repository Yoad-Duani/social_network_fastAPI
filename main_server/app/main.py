
from fastapi import FastAPI, HTTPException, status, Request
from colorama import init, Fore

# import sys, os, io

from app.models import Comment, Groups
from . import models
from .database import engine
from .routers import post,user, auth, vote, comment, groups
from fastapi.middleware.cors import CORSMiddleware
import datetime
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse
import json
from app import constants as const
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
#
#
#
from logging.config import dictConfig
import logging
# from .log_conf import LogConfig

# dictConfig(LogConfig().dict())
# logger = logging.getLogger("mycoolapp")

init(autoreset=True)
app = FastAPI(
    title= const.FASTAPI_METADATA_TITLE,
    version= const.FASTAPI_METADATA_VERSION,
    description= const.FASTAPI_METADATA_DESCRIPTION,
    contact= {
        "name": f"{const.FASTAPI_METADATA_CONTACT_NAME}",
        "url": "https://www.linkedin.com/in/yoad-duani/",
    },
)



app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins= const.ALLOW_ORIGINS,
    allow_credentials= True,
    allow_methods= const.ALLOW_METHODS,
    allow_headers=["*"],
)












app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comment.router)
app.include_router(groups.router)
app.include_router(post.router_group)

try:
    models.Base.metadata.create_all(bind=engine)
    print(Fore.GREEN + "INFO:     Database connection was seccesfull")
except Exception as error:
     print(Fore.RED + "Connection to database is failed")
     print(Fore.RED +"Error:  " , Fore.RED +  str(error))


@app.get("/")
async def root(request: Request):
    print(request.client.host)
    now = datetime.datetime.now()
    now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
    # logger.info("Dummy Info")
    return {
        "API Name": "Social Network fastAPI",
        "API Documentation": f"{request.url._url}docs",
        "GitHub Repo": "https://github.com/Yoad-Duani/social_network_fastAPI",
        "Host": f"{request.client.host}",
        "Date": F"{now}"
    }
    



@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
def validation_exception_handler(request, exc):
    print(f"The client sent invalid data: {exc}")
    exc_json = json.loads(exc.json())
    response = {"error type": "validation error" ,"message": [], "data": None}
    for error in exc_json:
        response['message'].append(error['loc'][-1]+f": {error['msg']}")
    return JSONResponse(response, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

