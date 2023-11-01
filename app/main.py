from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# Don't need anymore after we introduced Alembic for running db migrations
# models.Base.metadata.create_all(bind=engine) # creates all the tables specified in models.py - no action if the table exists

app = FastAPI() # create an instance of FastAPI

# origins = ["https://www.google.com", "https://www.youtube.com"] # ["*"] if it's a public API and should be universally accessible
origins = ["*"]

app.add_middleware(
    CORSMiddleware, # middleware = a function that runs before any request
    allow_origins=origins, # speicifies what domains are allowed to talk to our API
    allow_credentials=True,
    allow_methods=["*"], # for public APIs, we can restrict methods to GET only, for example
    allow_headers=["*"], # the same goes for headers
)

# A request first goes here and tries to find a route that matches
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to Kirill's API!"}
