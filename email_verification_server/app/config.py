from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_verify_service: str
    app_auth_token: str
    app_auth_token_prod: str = None
    skip_auth: bool = False

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()
    
settings = get_settings()