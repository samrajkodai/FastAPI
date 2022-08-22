from .. import models,schema
from fastapi import status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from .. import utils
from .. utils import hash
from .. import oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

User=schema.User
Login=schema.Login



router=APIRouter(prefix="/users",tags=['users'])

######### User Registration ###############
############################################


@router.post("/Create_User",status_code=status.HTTP_201_CREATED)

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


@router.get("/users/{id}")

def get_user(id: int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    
    if user==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="details not found"
        )
    return user


@router.post("/login")

def login(login: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    #OAuth2PasswordRequestForm
    #password

    user=db.query(models.User).filter(models.User.email==login.username).first()
    
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials"
        )
    
    
        
    if not utils.verify(login.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials"
        )
    
    access_token=oauth.create_access_token(data={"user_id":user.id})
        
    return {"token":access_token,'token_type':"bearer"}


