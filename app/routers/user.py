from typing import List
from .. import database, models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import autho2

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.response_user)
def create_users(user: schemas.user_create, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model= schemas.response_user)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail= f"the user with id {id} is not found")

    return user


@router.get('/',response_model= List[schemas.response_user])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user

@router.delete('/{id}')
def delete_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail= f'User with id {id} is not found')

    user.delete(synchronize_session = False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model= schemas.response_user)
def update_user(id:int,user: schemas.user_create, db: Session = Depends(get_db),
                current_user: int = Depends(autho2.get_current_user)):
    user.password = utils.hash_password(user.password)
    user_update = db.query(models.User).filter(models.User.id == id)

    if not user_update.first:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)

    user_update.update(user.dict(), synchronize_session= False)

    db.commit()
    
    return user_update.first()

    

  