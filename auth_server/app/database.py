from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from colorama import init, Fore
from .config import settings
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ServerSelectionTimeoutError
from app.log_config import init_loggers
import traceback

# from fastapi import status , HTTPException
log = init_loggers(logger_name="mongo-logger")

client = MongoClient(
            f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_url}:27017/{settings.mongodb_db_name}?authSource=admin",
            connect=True,
            serverSelectionTimeoutMS=5000,
            # tls=True,
        )

def check_mongodb_connection():
    global client
    log.info(f"Trying to connect to mongo.")
    try:
        mongo_response =  client.server_info()
        log.info(f"The connection to mongo was successful")
        return mongo_response
    except Exception as ex:
        log.error(f"An error occurred while connecting to mongo: {ex}")
        # log.debug(f"{traceback.format_exc()}")
        raise Exception(f"An error occurred while connecting to mongo: {ex}")
    # finally:
    #     client.close()





# init(autoreset=True)

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     except Exception as error:
#         print(Fore.RED + "Eror:")
#         print(Fore.RED + str(error))
#     finally:
#         db.close()
