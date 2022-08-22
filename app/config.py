from pydantic import BaseSettings


        
class Settings(BaseSettings):
    SERVER: str
    DATABASE: str
    DRIVER1: str

    class Config:
        env_file = ".env"

