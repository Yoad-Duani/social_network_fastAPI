import asyncio
from fastapi import FastAPI, Form, Cookie, status
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
from .config import settings

app = FastAPI()
client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

# @app.get("/")
# def root():
#     return {"message": "hello world"}

@app.get('/')
def index():
    return FileResponse('./app/index.html')


@app.post('/')
async def handle_form(email: str =  Form(...)):
    await asyncio.get_event_loop().run_in_executor(
        None, send_verification_code, email)
    response = RedirectResponse('/verify',
                                status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie('email', email)
    return response


def send_verification_code(email):
    verification = client.verify.services(
        settings.twilio_verify_service).verifications.create(
            to=email, channel='email')
    assert verification.status == 'pending'


@app.get('/verify')
async def verify():
    return FileResponse('./app/verify.html')

@app.post('/verify')
async def verify_code(email: str = Cookie(None), code: str = Form(...)):
    verified = await asyncio.get_event_loop().run_in_executor(
        None, check_verification_code, email, code)
    if verified:
        return RedirectResponse('/success',
                                status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse('/verify',
                                status_code=status.HTTP_303_SEE_OTHER)


def check_verification_code(email, code):
    verification = client.verify.services(
        settings.twilio_verify_service).verification_checks.create(
            to=email, code=code)
    return verification.status == 'approved'


@app.get('/success')
async def success():
    return FileResponse('./app/success.html')