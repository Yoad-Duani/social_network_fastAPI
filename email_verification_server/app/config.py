from pydantic import BaseSettings

class Settings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_verify_service: str

    class Config:
        env_file = '.env'

settings = Settings()