from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from app import models, schemas, utils
from app.database import engine, get_db
from app.routers import posts, users, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
    
# connecting to the postgres database
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='adi62000', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connected to the database successfully!")
#         break
#     except Exception as e:
#         print("Connection to the datavase failed")
#         print("error: ",e)
#         # if connection failed wait for 3 secs and retry.
#         time.sleep(3)
    

# store_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "Favourite Anime", "content": "One Piece", "id": 2}]

# def find_post(id):
#     """
#     find a post with a given id
#     """
#     for p in store_posts:
#         if p["id"] == id:
#             return p
        
# def find_index(id):
#     """
#     find the index of the post given it's index
#     """
#     for i, p in enumerate(store_posts):
#         if p["id"] == id:
#             return i
        
# order of these decorators matters.

@app.get("/")
def root():
    return {"messaege": "Hii! my name is Aditya!"}

# getting all posts

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)