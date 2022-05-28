from fastapi import FastAPI
from colorama import init, Fore

from app.models import Comment, Groups
from . import models
from .database import engine
from .routers import post,user, auth, vote, comment, groups
from fastapi.middleware.cors import CORSMiddleware


init(autoreset=True)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comment.router)
app.include_router(groups.router)
app.include_router(post.router_group)

try:
    models.Base.metadata.create_all(bind=engine)
    print(Fore.GREEN + "INFO:     Database connection was seccesfull")
except Exception as error:
     print(Fore.RED + "Connection to database is failed")
     print(Fore.RED +"Error:  " , Fore.RED +  str(error))


@app.get("/")
async def root():
    return {"message": "Hello World new update"}



