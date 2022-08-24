from fastapi import FastAPI,Depends

from app.routers.votes import votes
from . import models
from . database import Base, engine,get_db
from sqlalchemy.orm import Session
from . routers import post,user,votes
from typing import Optional
from . config import Settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(votes.router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

######### All Posts  ###############
#####################################

@app.get("/all")

def test(db: Session = Depends(get_db),limit: int =10,skip: int=0,search: Optional[str]=""):
    print(limit)
    posts=db.query(models.User ).filter(models.User.email.contains(search)).limit(limit=limit).all()
    return posts
