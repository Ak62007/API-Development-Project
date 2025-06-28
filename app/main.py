from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# let's define a structure
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

store_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "Favourite Anime", "content": "One Piece", "id": 2}]

def find_post(id):
    """
    find a post with a given id
    """
    for p in store_posts:
        if p["id"] == id:
            return p
        
def find_index(id):
    """
    find the index of the post given it's index
    """
    for i, p in enumerate(store_posts):
        if p["id"] == id:
            return i
        
# order of these decorators matters.

@app.get("/")
def root():
    return {"messaege": "Hii! my name is Aditya!"}

# getting all posts

@app.get("/posts")
def get_posts():
    return {"data" : store_posts}

# creating a post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 100000)
    store_posts.append(post_dict)
    return {"data" : post_dict}

# getting an individual post

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The post with id: {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"The post with id: {id} is not found"}
    return {"data": post}

# Deleting a post with an id

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id:{id} was not found")
    store_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int, post: Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id: {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    store_posts[index] = post_dict
    return{"updated post": post_dict}