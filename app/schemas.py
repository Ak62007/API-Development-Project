from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class CreatePost(PostBase):
    pass

# post response model
class Post(PostBase):
    id: int
    created_at: datetime
    
    # we need to provide this because pydantic will have no idea about sqlalchemy schemas this lets pydantic know that it is sqlalchemy model and go ahead and convert it into pydantic model. usually pydantic expects dictionary to be passed to it to convert it into pydantic model.
    class Config:
        orm_mode = True

# user responce model        
class UserRes(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    