import email
from typing import Optional
from pydantic import BaseModel,EmailStr
from pydantic.types import conint

class Post(BaseModel):  # pydantic for schema
    name: str
    age: int
    user_id: int
    # published: bool = True

class User(BaseModel):  # pydantic for schema
    email: EmailStr
    password: str
    # published: bool = True

class Login(BaseModel):
    email: EmailStr
    password: str
    
class TokenData(BaseModel):
    id: Optional[str]=None
    
class Vote(BaseModel):
    post_id: int
    dir:conint(le=1)