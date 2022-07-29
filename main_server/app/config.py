from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str 
    database_password: str 
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # email_username: str
    # email_password: str
    # email_from: str

    class Config:
        env_file = ".env"

settings = Settings()