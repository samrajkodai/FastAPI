from pydantic import BaseModel,EmailStr

class Post(BaseModel):  # pydantic for schema
    name: str
    age: int
    # published: bool = True

class User(BaseModel):  # pydantic for schema
    email: EmailStr
    password: str
    # published: bool = True
