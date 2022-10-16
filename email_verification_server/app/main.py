# from urllib.request import Request
from fastapi import Body, FastAPI, Form, Cookie, status, Query, Header, HTTPException, Request, BackgroundTasks
from fastapi.responses import FileResponse, RedirectResponse, Response
from twilio.rest import Client
from .config import settings
from pydantic import Required
from pathlib import Path
from .routers import verify_mail
from fastapi.responses import JSONResponse

from .oauth2 import verify_token
from starlette.responses import HTMLResponse
from fastapi.responses import HTMLResponse
from .emails import *

from fastapi.templating import Jinja2Templates
from .database import client

from colorama import init, Fore

from . import schemas




from fastapi import FastAPI
# import connection
from bson import ObjectId
# from schematics.models import Model

init(autoreset=True)
app = FastAPI()
app.include_router(verify_mail.router)




try:
    client.server_info()
    print(Fore.GREEN + "INFO:     MongoDB database connection was seccesfull")
except Exception as error:
     print(Fore.RED + "Connection to MongoDB database is failed")
     print(Fore.RED +"Error:  " , Fore.RED +  str(error))





templates = Jinja2Templates(directory= Path(__file__).parent / 'templates')



@app.get('/')
def index():
    return {"message": "test"}



@app.post('/verify-test')
async def email_verification_mail(background_tasks: BackgroundTasks)-> JSONResponse:
    background_tasks.add_task(send_email, {"email": "yoad787@gmail.com", "user_id": 999, "name": "Yoad"})
    



@app.get('/verify-test')
async def email_verification(request: Request, token: str):
    user = await verify_token(token)

    if user.get("id"):
        #send a request to update user
        print("sccuess verify user mail!")
        return templates.TemplateResponse("verified_mail.html", {"request": request, "name": user.get("name")})
        pass
