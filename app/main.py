
from cgitb import reset
from distutils.log import error
import imp
from unicodedata import name
from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
import random
import pyodbc
import pandas as pd
from . import models
from . database import engine,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

try:
        
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=MSI\SQLEXPRESS;'
                        'Database=Fastapi;'
                        'Trusted_Connection=yes;')
    
    cursor = conn.cursor()
    
    MY_TABLE="fast_info"


except error as err:
    print("err :",err)
    
    

######### POST METHOD ###############
#####################################

class Post(BaseModel):  # pydantic for schema
    name: str
    age: int
    # published: bool = True



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
    
        conn.commit() 
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


######### Database Connetion ###############
############################################
