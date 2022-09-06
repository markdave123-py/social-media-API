
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, autho,votes
from .config import settings
# models.base.metadata.create_all(bind= engine)


from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI()

origins= ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(autho.router)
app.include_router(votes.router)
  

@app.get('/')
def simple():
    return {'message': 'sucess'}










    

    
