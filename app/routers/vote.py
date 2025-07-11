from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, database, oauth2, models


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Let's first check if the post exists
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} is not found")
    
    vote_query = db.query(models.Votes).filter(vote.post_id == models.Votes.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with id: {current_user.id} already voted on post with id: {vote.post_id}")
        new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully voted!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote!"}