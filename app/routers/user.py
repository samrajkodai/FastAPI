
from ctypes import util
from .. import models,schema
from fastapi import status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import engine,get_db
from .. import utils
from .. utils import hash

User=schema.User
Login=schema.Login

User_Router=APIRouter(prefix="/users",tags=['users'])

######### User Registration ###############
############################################


@User_Router.post("/Create_User",status_code=status.HTTP_201_CREATED)

def create_user(post: User,db: Session = Depends(get_db)):
    password=post.password
    password=hash(password)
    post=post.dict()
    post.update({"password":password})
    createpost=models.User(**post)
    print(createpost)
    db.add(createpost)
    db.commit()
    db.refresh(createpost)
    
    if createpost==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="not created"
        )
    return createpost


@User_Router.get("/users/{id}")

def get_user(id: int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    
    if user==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="details not found"
        )
    return user


@User_Router.post("/login")


def login(login: Login,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==login.email).first()
    
    print(user.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials"
        )
    
    
        
    if not utils.verify(login.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials"
        )
    
    return {"token":"example token"}
