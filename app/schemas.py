from datetime import datetime

from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class Post(BaseModel):
    title:str
    content: str
    published: bool = True

class response_user(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class Post_create(Post):
    class Config:
        orm_mode = True


class Response(Post):
    created_at: datetime
    owner_id: int
    id: int 

    owner: response_user


    class Config:
        orm_mode = True

    

class Postout(BaseModel):
   
    Post: Response
    votes: int

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None


    class Config:
        orm_mode = True

class user_create(BaseModel):
    email:EmailStr
    password: str

    
class user_login(BaseModel):
    email: EmailStr
    password: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
