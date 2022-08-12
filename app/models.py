from . database import Base
from sqlalchemy import Column,Integer,String

class TaskDB(Base):
    __tablename__="posts"
    
    id=Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)