from fastapi import FastAPI,APIRouter,status,Depends,HTTPException
from .. import schema,database,models
from sqlalchemy.orm import Session

router=APIRouter(prefix='/votes',tags=['vote'])


@router.post('/votes',status_code=status.HTTP_201_CREATED)

def votes(vote:schema.Vote,db: Session = Depends(database.get_db)):
    vote_query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id)
    found_vote=vote_query.first()
    if vote.dir==1:
        
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already voted on post")
        
        
    return {"vote":"successful"}