from os import stat
from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schema
from fastapi.security.oauth2 import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi import status, HTTPException,Depends,APIRouter
#secret key
#algorithm
#expire time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode=data.copy()
    
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
    
    
def verify_access_token(token: str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    
        id:str=payload.get("user_id")
        
        
        if not id:
            raise credentials_exception
        
        token_data=schema.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str =Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
    
    
    return verify_access_token(token,credentials_exception)