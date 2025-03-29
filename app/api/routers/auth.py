import os
import secrets

from fastapi import APIRouter, Depends, status, HTTPException, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from authx import AuthX, AuthXConfig
from sqlalchemy import select

from app.models import User
from app.db import create_session, user_exists
from app.utils import get_hashed_password, verify_password
from app.schemas import UserResponse, UserCreate, RefreshData

auth_route = APIRouter(prefix='/auth', tags=['Авторизация'])

config = AuthXConfig(
    JWT_ALGORITHM=os.getenv('JWT_ALGORITHM', default='HS256'),
    JWT_SECRET_KEY=os.getenv(
        'JWT_SECRET_KEY', default='secret_key',
    ),
    JWT_TOKEN_LOCATION=['cookies'],
    JWT_COOKIE_CSRF_PROTECT=False
)

auth = AuthX(config=config)


@auth_route.post('/register', response_model=UserResponse)
async def register(
    data: UserCreate, session: AsyncSession = Depends(create_session)
):

    if await user_exists(User, data.email):
        return HTTPException(400, detail='User already exists')

    user = User(
        email=data.email,
        password=get_hashed_password(data.password)
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@auth_route.post('/login')
async def login(
    data: UserCreate, session: AsyncSession = Depends(create_session)
):
    email = data.email

    user_query = select(User).where(User.email == email)
    result = await session.execute(user_query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(404, detail={'message': 'User does not exist'})

    if not verify_password(data.password, user.password):
        raise HTTPException(401, detail={'message': 'Invalid password'})

    token = auth.create_access_token(uid=user.email)
    response = JSONResponse(content={'access_token': token})
    response.set_cookie(
        key="access_token_cookie",
        value=token,
        httponly=True
    )
    return response


@auth_route.post(
    '/refresh',
    status_code=status.HTTP_201_CREATED
)
async def refresh_token(
    refresh_token_cookie: str = Cookie(None), refresh_data: RefreshData = None
):
    try:
        token = refresh_token_cookie or (refresh_data and refresh_data.refresh_token)
        if not token:
            raise HTTPException(
                status_code=401, detail='Missing refresh token'
            )

        refresh_payload = auth.verify_token(token, verify_type=True)

        access_token = auth.create_access_token(refresh_payload.sub)
        response = JSONResponse(content={'access_token': access_token})
        response.set_cookie(
            key="access_token_cookie",
            value=token,
            httponly=True
        )
        return response

    except Exception as e:
        print(f"Error in refresh_token: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))