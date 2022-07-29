from unicodedata import name
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import join, text, true
# from sqlalchemy.sql.functions import user
# from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default= 'True', nullable= False)
    created_at = Column(TIMESTAMP(timezone= True),nullable= False, server_default= text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable= False,)
    group_id = Column(Integer,server_default = '0', nullable= False) 
    owner = relationship("User")
    comments = relationship("Comment")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True),nullable= False, server_default= text('now()'))
    name = Column(String, nullable= False) 
    birth_date = Column(Date, nullable= False) 
    is_blocked = Column(Boolean, server_default= 'False', nullable= False) 
    update_at = Column(TIMESTAMP(timezone= True), server_default= text('now()'), nullable= False)
    verified = Column(Boolean, server_default= 'False', nullable= False)
    company_name = Column(String, server_default="No Company", nullable= False)
    description = Column(String, server_default= "No Description", nullable= False)
    position = Column(String, server_default= "No Position", nullable= False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    
class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key= True, nullable= False)
    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    content = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True),nullable= False, server_default= text('now()'))
    update_at = Column(TIMESTAMP(timezone= True),nullable= False, server_default= text('now()'))

class Groups(Base):
    __tablename__ = "groups"
    groups_id = Column(Integer, primary_key= True, nullable= False)
    creator_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE"))
    name = Column(String, nullable= False) 
    description= Column(String, nullable= False) 
    group_private= Column(Boolean, server_default= 'False', nullable= False)
    created_at= Column(TIMESTAMP(timezone= True),nullable= False, server_default= text('now()'))
    update_at= Column(TIMESTAMP(timezone= True),nullable= False, server_default= text('now()'))

class UserInGroups(Base):
    __tablename__ = "usersInGroups"
    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE"), primary_key=True)
    groups_id = Column(Integer, ForeignKey("groups.groups_id", onupdate="CASCADE"), primary_key=True)
    is_blocked = Column(Boolean, server_default= 'False', nullable= False)
    # request_accepted = Column(Boolean, server_default= 'False', nullable= False)
    # update_at= Column(TIMESTAMP(timezone= True),nullable= False, server_default= text('now()'))
    join_group_date = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('now()'))

class JoinRequestGroups(Base):
    __tablename__ = "JoinRequestGroups"
    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE"), primary_key=True)
    groups_id = Column(Integer, ForeignKey("groups.groups_id", onupdate="CASCADE"), primary_key=True)
    name = Column(String, nullable= False)
    group_name = Column(String, nullable= False)