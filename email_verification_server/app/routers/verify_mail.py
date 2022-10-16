from fastapi import Body, FastAPI, Path, Query , Response ,status , HTTPException, Depends, APIRouter
from .. import schemas
from ..database import client

# router = APIRouter(
#     prefix= "/email-verification",
#     tags= ['email-verification']
#     )

router = APIRouter(
    prefix= "/user-test",
    tags= ['user-test']
    )

@router.get('/')
async def create_user():
    info = client.server_info()
    print(info )
    return info

# @router.post('/')
# async def create_ser():
