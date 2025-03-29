from fastapi import APIRouter, Depends, status
from sqlalchemy import select

from fasapi_audio_loader.app.models import User
from app.api.routers.auth import auth

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get(
    '/{user_id}',  response_model=User, status_code=status.HTTP_200_OK
)
async def get_user(user_id: int):
    pass


@router.put(
    '/{user_id}', dependencies=[Depends(auth.access_token_required)],
    response_model=User, status_code=status.HTTP_201_CREATED
)
async def change_user(user_id: int):
    pass


@router.delete(
    '/{user_id}', dependencies=[Depends(auth.access_token_required)],
    response_model=User, status_code=status.HTTP_201_CREATED
)
async def delete_user(user_id: int):
    pass
