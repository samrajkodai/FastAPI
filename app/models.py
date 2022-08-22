from . database import Base
from sqlalchemy import Column,Integer,String,ForeignKey

class TaskDB(Base):
    __tablename__="posts"
    
    id=Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)
    user_id=Column(Integer,ForeignKey("User_Info.id",ondelete="CASCADE"),nullable=False)
    # published=Column(Boolean, unique=False, default=True)
    
    
class User(Base):
    __tablename__="User_Info"
    
    id=Column(Integer,primary_key=True)
    email=Column(String)
    password=Column(String)
