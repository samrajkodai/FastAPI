from ast import Del
from pydoc import classname
import re
from telnetlib import DET
from this import d
from urllib import response
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import random

app=FastAPI()

@app.get("/")

async def main():
    return {"name":"samraj"}


@app.get("/post")

def home():
    return {"data":"post"}


######### POST METHOD ###############
#####################################

class Post(BaseModel): #pydantic for schema
    name: str
    age: int
    published: bool=True


my_posts=[]

@app.post("/posts",status_code=201)

def home(post:Post):
    id=random.randint(1,1000)
    post=post.dict()
    post["id"]=id
    my_posts.append(post)


    return {"data":my_posts}



######### get indidual post using id ###############
####################################################


class FastAPI:
    def __init__(self,id):
        self.id=id
    
    def find_post(self):
        print("self.id",self.id)
        result=[i  if i["id"]==self.id else "not found" for i in my_posts]

        return result

    def delete(self):
        print("self.id",self.id)
        result=[my_posts.pop(i) if i["id"]==self.id else "id not found" for i in my_posts]
        
        return result

@app.get("/getpost/{id}")

def getpost(id: int):
    print(type(id))
    api=FastAPI(id)

    post=api.find_post()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
        
    return {"result":post}

 
######### Delete post ###############
#####################################


@app.delete("/delete/{id}")

def delete(id: int):
    api=FastAPI(id)
    print(api.delete())

    Delete=api.delete()
    # for i in Delete:
    #     print(i)
    #     Delete=my_posts.pop(i)
    
    # Delete=my_posts.pop(Delete[0])
    return {"result":Delete}