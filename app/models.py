from email.policy import default
from psycopg2 import Timestamp
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .database import base 
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.sql.expression import  text

class Post(base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default= 'True')
    created_at = Column(TIMESTAMP(timezone=True), server_default= text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(base):
    __tablename__ = 'users'

    email = Column(String, unique= True, nullable= False)
    id = Column(Integer, primary_key=True, nullable=False)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), server_default= text('now()'), nullable=False)


class Vote(base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True)