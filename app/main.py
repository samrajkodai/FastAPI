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
from . routers import post,user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.Router)
app.include_router(user.Router)

######### All Posts  ###############
#####################################

@app.get("/all")

def test(db: Session = Depends(get_db)):
    posts=db.query(models.TaskDB ).all()
    return posts


