# from unicodedata import name
# from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import join, text, true
# from sqlalchemy.sql.functions import user
# from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import TIMESTAMP
# from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum

# class User(Base):
#     __tablename__ = "users_auth"
#     id = Column(Integer, primary_key= True, nullable= False)
#     email = Column(String, nullable= False, unique= True)
#     password = Column(String, nullable= False) 
#     is_blocked = Column(Boolean, server_default= 'False', nullable= False) 
#     password_update_at = Column(TIMESTAMP(timezone= True), server_default= text('now()'), nullable= False)
#     verified = Column(Boolean, server_default= 'False', nullable= False)

def user_serializer(user) -> dict:
    return{
        "id": str(user["_id"]),
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"]
    }


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]