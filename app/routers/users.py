from app import schemas, models, utils
from app.database import get_db
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    
    # hash the user's password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserRes)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found!")
    return user

