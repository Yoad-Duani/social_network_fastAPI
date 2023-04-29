from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # Keycloak
    keycloak_port: int
    keycloak_hostname: str
    auth_server_url: str
    client_id: str
    client_secret: str
    admin_client_secret: str
    realm: str
    keycloak_port_callback: int
    login_uri: str

    # Mongodb
    mongodb_username: str
    mongodb_password: str
    mongodb_url: str
    mongodb_db_name: str

    # Email
    mail_username: str
    mail_password: str
    mail_auth_token_key: str
    mail_token_algorithm: str
    mail_port: int
    mail_token_expire_hours: int


    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
    
settings = get_settings()