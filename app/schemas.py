from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

# PostBase class for data validation (pydantic model)
# Defining a shape of our request
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    # To convert SQLAlchemy model to ORM model, converting it to dictionary
    class Config:
        from_attributes = True

# I resolved the Validation error (title and content) by changing the inheritance from PostBase to BaseModel here
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)
