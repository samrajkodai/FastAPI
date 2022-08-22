from .. import models,schema,oauth
from fastapi import Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import get_db 

######### POST METHOD ###############
#####################################
router=APIRouter(prefix="/posts",tags=['posts'])


Post=schema.Post




@router.post("/posts", status_code=201)
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

@router.get("/getpost/{id}")
def getpost(id: int,db: Session = Depends(get_db)):
    res=db.query(models.TaskDB ).filter(models.TaskDB.id==id).first()
    print(res)
         
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    
 
        
    return {"result": res}


######### Delete post ###############
#####################################


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int,db: Session = Depends(get_db),user_id: int= Depends(oauth.get_current_user)):
    
    try:
        if user_id==oauth.get_current_user.id:
            post=db.query(models.TaskDB ).filter(models.TaskDB.id==id)
            
            post.delete()
        
            db.commit()
            
        else:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to delete the post")
        
    except:
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


######### update post ###############
#####################################


@router.put("/update/{id}")
def update(id: int, post: Post,db: Session = Depends(get_db),user_id: int= Depends(oauth.get_current_user)):
    
    demo=str(post.name)
    print(demo)
    MY_TABLE="fast_info"
    try:
        if user_id==oauth.get_current_user.id:
            post_query=db.query(models.TaskDB ).filter(models.TaskDB.id==id)
            post_query.update(post.dict())
            db.commit()
            
        else:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to delete the post")
       
        
        
        
    except :
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

    return {"post": "res"}
