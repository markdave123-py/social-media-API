from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import database, models,schemas
from .. import autho2
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)




@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.Response)
def create_post(post: schemas.Post_create, db: Session = Depends(get_db), 
                current_user: int = Depends(autho2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id,**post.dict())
   
    db.add(new_post)
    db.commit()

    db.refresh(new_post)

    return new_post


@router.get('/', response_model= List[schemas.Postout])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(autho2.get_current_user),
                        limit:int = 20, skip:int =0,search:Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.get('/{id}', response_model=  schemas.Postout)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(autho2.get_current_user)):
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post of id {id} not found")

    return post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), 
                        current_user: int = Depends(autho2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post of id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Not authorizated to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put('/{id}', response_model= schemas.Response)
def update_post(id: int,updated_post: schemas.Post, db: Session = Depends(get_db)
                ,current_user: int = Depends(autho2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"post of id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Not authorizated to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

   