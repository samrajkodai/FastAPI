import string
from . database import Base
from sqlalchemy import Column,Integer,String

class TaskDB(Base):
    __tablename__="posts"
    
    id=Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)
    # published=Column(Boolean, unique=False, default=True)
    
    
class User(Base):
    __tablename__="User_Info"
    
    id=Column(Integer,primary_key=True)
    email=Column(String)
    password=Column(String)
