from pydantic import BaseModel

class Post(BaseModel):  # pydantic for schema
    name: str
    age: int
    # published: bool = True

