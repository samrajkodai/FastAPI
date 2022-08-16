
from .post import Router
from .. import models,schema
from fastapi import status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import engine,get_db

User=schema.User
Router=APIRouter(prefix="/users",tags=['users'])

######### User Registration ###############
############################################


@Router.post("/Create_User",status_code=status.HTTP_201_CREATED)

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


@Router.get("/users/{id}")

def get_user(id: int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    
    if user==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="details not found"
        )
    return user
    