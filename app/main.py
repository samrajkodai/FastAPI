
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
    
    
@app.get("/sql")

def test(db: Session = Depends(get_db)):
    posts=db.query(models.TaskDB ).all()
    return {"status":posts}

@app.get("/")
async def main():
    return {"name": "samraj"}


@app.get("/post")
def home():
    return {"data": my_posts}


######### POST METHOD ###############
#####################################

class Post(BaseModel):  # pydantic for schema
    name: str
    age: int
    published: bool = True



@app.post("/posts", status_code=201)
def home(post: Post,db: Session = Depends(get_db)):   
    result=models.TaskDB(id=random.randint(1,10000),name=post.name,age=post.age)
    db.add(result)
    db.commit()
    db.refresh(result)
    return {"data": result}


######### get indidual post using id ###############
####################################################
class FastAPI:
    def __init__(self, id):
        self.id = id

    def find_post(self):
        result = [i if i["id"] == self.id else "not found" for i in my_posts]
        return result

    def delete(self):
        result = [my_posts.pop(
            i) if p["id"] == self.id else "id not found" for i, p in enumerate(my_posts)]
        return result


class Update(FastAPI):
    def __init__(self, id, post):
        super().__init__(id)
        self.post = post

    def update(self):
        result = [i.update(self.post) if i["id"] ==
                  self.id else "id not found" for i in my_posts]
        return result


@app.get("/getpost/{id}")
def getpost(id: int):
    MY_TABLE="fast_info"
    cursor.execute(f"select * from {MY_TABLE} where id={id}")
    
    res= None
    for i in cursor:
        # res=cursor.fetchone()
        print(i[0])
        print(i[1])
        print(i[2])   
        res=i[0],i[1],i[2]
            
    print((res))
    conn.commit()
    
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    
 
        
    return {"result": res}


######### Delete post ###############
#####################################


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    
    try:
        cursor.execute(f"Delete from {MY_TABLE} where id={id}")
    
        conn.commit()
        
    except:
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


######### update post ###############
#####################################


@app.put("/update/{id}")
def update(id: int, post: Post):
    
    demo=str(post.name)
    print(demo)
    MY_TABLE="fast_info"
    try:
        cursor.execute(f'''
                UPDATE {MY_TABLE}
                SET id = {id},
                names='{demo}',
                age={post.age}
                WHERE id = {id}
                ''')
        
        cursor.execute(f"select * from {MY_TABLE} where id={id}")
        res= None
        for i in cursor:
            # res=cursor.fetchone()
            print(i[0])
            print(i[1])
            print(i[2])   
            res=i[0],i[1],i[2]
    
        conn.commit()
        
        
        
    except pyodbc.Error  as err:
        
        print(err)

    if res==None:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

    return {"post": res}


######### Database Connetion ###############
############################################
