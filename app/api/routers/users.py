from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.db import create_session, get_user
from app.utils import superuser_required
from app.schemas import UserResponse


users_route = APIRouter(prefix='/users', tags=['Пользователи'])


@users_route.get(
    '/', response_model=list[UserResponse],
    status_code=status.HTTP_200_OK
)
async def list_users(
    session: AsyncSession = Depends(create_session)
):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@users_route.get(
    '/{user_id}',  response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(create_session)
):

    user = await get_user(User, user_id, session)

    if not user:
        return HTTPException(400, detail='User already exists')

    return user


@users_route.put(
    '/{user_id}', dependencies=[Depends(superuser_required)],
    response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def change_user(user_id: int):
    pass


@users_route.delete(
    '/{user_id}', dependencies=[Depends(superuser_required)],
    response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def delete_user(
    user_id: int, session: AsyncSession = Depends(create_session)
):

    user = await get_user(User, user_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    user_data = {
        'id': user.id,
        'email': user.email,
        'audios': user.audios
    }

    await session.delete(user)
    await session.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'message': 'User successfully deleted',
            'deleted_user': user_data
        }
    )
