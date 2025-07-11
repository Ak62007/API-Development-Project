from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
# user responce model        
class UserRes(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class CreatePost(PostBase):
    pass

# post response model
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserRes
    
    # we need to provide this because pydantic will have no idea about sqlalchemy schemas this lets pydantic know that it is sqlalchemy model and go ahead and convert it into pydantic model. usually pydantic expects dictionary to be passed to it to convert it into pydantic model.
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Posts: Post
    votes: int

        
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]