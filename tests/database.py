# from fastapi.testclient import TestClient
# import pytest
# from app.main import app
# from app.config import settings
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from app.database import get_db
# from app.database import Base
# from colorama import init, Fore


# init(autoreset=True)

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)



# @pytest.fixture
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     except Exception as error:
#         print(Fore.RED + "Eror:")
#         print(Fore.RED + str(error))
#     finally:
#         db.close()


# @pytest.fixture
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         except Exception as error:
#             print(Fore.RED + "Eror:")
#             print(Fore.RED + str(error))
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)