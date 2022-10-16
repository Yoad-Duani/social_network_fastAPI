from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # twilio_account_sid: str
    # twilio_auth_token: str
    # twilio_verify_service: str
    # app_auth_token: str
    # app_auth_token_prod: str = None
    # skip_auth: bool = False

    mail_username: str
    mail_password: str

    mail_auth_token_key: str
    mail_token_algorithm: str
    mail_port: int
    mail_token_expire_hours: int

    mongodb_url: str

    mongodb_username: str
    mongodb_password: str
    mongodb_url: str
    mongodb_db_name: str

    
    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()
    
settings = get_settings()