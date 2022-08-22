from fastapi import FastAPI,Depends
from . import models
from . database import Base, engine,get_db
from sqlalchemy.orm import Session
from . routers import post,user
from typing import Optional
from . config import Settings

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)


######### All Posts  ###############
#####################################

@app.get("/all")

def test(db: Session = Depends(get_db),limit: int =10,skip: int=0,search: Optional[str]=""):
    print(limit)
    posts=db.query(models.User ).filter(models.User.email.contains(search)).limit(limit=limit).all()
    return posts
