from database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from datetime import datetime
class Post(Base):
    __tablename__="posts"
    
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String(255),nullable=False)
    content=Column(String(255),nullable=False)
    published=Column(Boolean,server_default=text("'1'"))
    created_at=Column(DateTime,nullable=False,default=datetime.utcnow)

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    username=Column(String(255),nullable=False)
    full_name=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False)
    hashed_password=Column(String(255),nullable=False)
    disabled=Column(Boolean,server_default=text("'0'"))
        