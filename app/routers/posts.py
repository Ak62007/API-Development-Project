from app import schemas, models
from app.database import get_db
from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts"
)

@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts
# doing it using pure sql and postgres driver
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"data" : posts}

# creating a post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    # creating the new post using unpacking.
    new_post = models.Posts(**post.dict())
    # new_post = models.Posts(title=post.title, content=post.content, published=post.published)
    db.add(new_post) # the post to the database
    db.commit() # commit the changes
    db.refresh(new_post) # extracts the newly created post and assigns it to new_posts.
    return new_post
    
    
# Doing it using pure sql and postgres driver
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data" : new_post}

# getting an individual post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Posts).filter(models.Posts.id == id)
    post = query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
    return post

# Using pure sql and using sql drivers    
    # try:
    #     cursor.execute("""SELECT * FROM posts WHERE post_id = %s""",(str(id)))
    #     post = cursor.fetchone()
    #     print("successfully got the post")
    #     return {'post': post}
    # except Exception as e:
    #     print("post not found")
    #     print("error: ",e)
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"The post with id: {id} is not found")
        
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"The post with id: {id} is not found")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"The post with id: {id} is not found"}
    # return {"data": post}

# Deleting a post with an id

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Posts).filter(models.Posts.id == id)
# Using pure sql and using sql drivers     
    # cursor.execute("""DELETE FROM posts WHERE post_id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id:{id} was not found")
    # chain the query with delete method to delete the post
    query.delete(synchronize_session=False)
    # commit the changes
    db.commit()
    
    print("deleted post successfully")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

        
    # index = find_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id:{id} was not found")
    # store_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):
    query = db.query(models.Posts).filter(models.Posts.id == id)
# Using pure sql and using sql drivers   
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    # chaining update function, pass the update as a dictionary
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    print("updated post successfully!")
    print("updated_post : ", query.first())
    return query.first()


    # index = find_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id: {id} not found")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # store_posts[index] = post_dict
    # return{"updated post": post_dict}