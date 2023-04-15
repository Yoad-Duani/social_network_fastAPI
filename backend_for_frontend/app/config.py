from pydantic import BaseSettings

class Settings(BaseSettings):
    auth_service_url: str
    main_service_url: str
    auth_service_port: str
    main_service_port: str

    class Config:
        env_file = ".env"

settings = Settings()