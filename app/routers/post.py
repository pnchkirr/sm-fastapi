from ..  import models, schemas
from ..database import get_db
from fastapi import status, Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import oauth2

# to make @app work correctly: @app ---> @router
router = APIRouter(
    prefix="/posts", # to abstain from writing "/posts" every single time
    tags=['Posts'] # structures docs, putting requests in this file under the same category
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post = models.Post(user_id=current_user.id, **post.model_dump()) # unpacking the dict so we don't have to specify all the fields
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post # to send back a dictionary

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              offset: int = 0,
              search: Optional[str] = ""):
    # print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

# select
# 	p.*,
# 	count(v.post_id) as votes
# from posts p
# left join votes v
#   on v.post_id = p.id
# group by p.id
# order by votes desc
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all() # to restrict users to their own posts only
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()