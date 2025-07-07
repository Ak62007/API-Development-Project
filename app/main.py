from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import posts, users, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"messaege": "Hii! my name is Aditya!"}

# connecting Routes
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)