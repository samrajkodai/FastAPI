from os import stat
from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.params import Body
import random
import pyodbc
import pandas as pd
from . import models
from . database import engine,get_db
from sqlalchemy.orm import Session
from . import schema
from . utils import hash

models.Base.metadata.create_all(bind=engine)


Post=schema.Post
User=schema.User

app = FastAPI()

######### All Posts  ###############
#####################################

@app.get("/all")

def test(db: Session = Depends(get_db)):
    posts=db.query(models.TaskDB ).all()
    return posts

######### POST METHOD ###############
#####################################



@app.post("/posts", status_code=201)
def home(post: Post,db: Session = Depends(get_db)):  
    print(post.dict()) 
    result=models.TaskDB(**post.dict())
    print(result)
    db.add(result)
    db.commit()
    db.refresh(result)
    return {"data": result}


######### get indidual post using id ###############
####################################################

@app.get("/getpost/{id}")
def getpost(id: int,db: Session = Depends(get_db)):
    res=db.query(models.TaskDB ).filter(models.TaskDB.id==id).first()
    print(res)
         
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    
 
        
    return {"result": res}


######### Delete post ###############
#####################################


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int,db: Session = Depends(get_db)):
    
    try:
        post=db.query(models.TaskDB ).filter(models.TaskDB.id==id)
        
        post.delete()
    
        db.commit()
        
    except:
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


######### update post ###############
#####################################


@app.put("/update/{id}")
def update(id: int, post: Post,db: Session = Depends(get_db)):
    
    demo=str(post.name)
    print(demo)
    MY_TABLE="fast_info"
    try:
        post_query=db.query(models.TaskDB ).filter(models.TaskDB.id==id)
        post_query.update(post.dict())
        db.commit()
        
        
        
    except pyodbc.Error  as err:
        
        print(err)
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

    return {"post": "res"}


######### User Registration ###############
############################################


@app.post("/Create_User",status_code=status.HTTP_201_CREATED)

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


@app.get("/users/{id}")

def get_user(id: int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    
    if user==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="details not found"
        )
    return user
    