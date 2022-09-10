import asyncio
from fastapi import Body, FastAPI, Form, Cookie, status, Query, Header, HTTPException
from fastapi.responses import FileResponse, RedirectResponse, Response
from twilio.rest import Client
from .config import settings
from pydantic import Required

from . import schemas

app = FastAPI()
client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

# @app.get("/")
# def root():
#     return {"message": "hello world"}

# APP_AUTH_TOKEN = settings.app_auth_token

@app.get('/')
def index():
    # return FileResponse('./app/index.html')
    return {"message": "test"}



def verify_auth(authorization = Header(None), settings = settings):
    if settings.skip_auth:
        return
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid endpoint")
    label, token = authorization.split()
    if token != settings.app_auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid endpoint")



@app.post('/')
async def handle_form(user: schemas.UserVerify = Body(default= Required), authorization = Header(None)):
    verify_auth(authorization)
    await asyncio.get_event_loop().run_in_executor(
        None, send_verification_code, user.email)
    # response = RedirectResponse('/verify', status_code=status.HTTP_303_SEE_OTHER)
    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie('email', user.email)
    return response


def send_verification_code(email):
    verification = client.verify.services(
        settings.twilio_verify_service).verifications.create(
            to=email, channel='email')
    assert verification.status == 'pending'


# @app.get('/verify')
# async def verify():
#     return FileResponse('./app/verify.html')


@app.get('/verify/{code}')
async def verify_code(code: int, email: str = Cookie(None)):
    print(email)
    verified = await asyncio.get_event_loop().run_in_executor(
        None, check_verification_code, email, code)
    if verified:
        return Response(content="success", status_code= status.HTTP_202_ACCEPTED)
        # return RedirectResponse('/success', status_code=status.HTTP_303_SEE_OTHER)
    else:
        return Response(content="faield", status_code= status.HTTP_406_NOT_ACCEPTABLE)
        # return RedirectResponse('/verify', status_code=status.HTTP_303_SEE_OTHER)



@app.post('/verify')
async def verify_code(code: schemas.CodeVerify, email: str = Cookie(None)):
    verified = await asyncio.get_event_loop().run_in_executor(
        None, check_verification_code, email, code.code)
    if verified:
        return Response(content="success", status_code= status.HTTP_202_ACCEPTED)
        # return RedirectResponse('/success', status_code=status.HTTP_303_SEE_OTHER)
    else:
        return Response(content="faield", status_code= status.HTTP_406_NOT_ACCEPTABLE)
        # return RedirectResponse('/verify', status_code=status.HTTP_303_SEE_OTHER)





def check_verification_code(email, code):
    verification = client.verify.services(
        settings.twilio_verify_service).verification_checks.create(
            to=email, code=code)
    return verification.status == 'approved'


# @app.get('/success')
# async def success():
#     return FileResponse('./app/success.html')