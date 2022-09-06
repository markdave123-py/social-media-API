from operator import mod
from fastapi import APIRouter, Depends,status,Response,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,utils,models,database
from .. import autho2
from sqlalchemy.orm import Session

router = APIRouter(tags=['authentication'])

@router.post('/login')
def login_user(user_crendentials: OAuth2PasswordRequestForm = Depends(),
                 db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_crendentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')

    if not utils.verify(user_crendentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')

    acess_token = autho2.create_token(data= {'user_id':user.id })

    return {"acess_token": acess_token, "token_type": "bearer"}



    






