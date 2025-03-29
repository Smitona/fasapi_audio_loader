import os
import secrets

from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from authx import AuthX, AuthXConfig
from authx_extra.oauth2 import MiddlewareOauth2
from sqlalchemy import select

from fasapi_audio_loader.app.models import User
from app.main import app
from app.db import create_session, user_exists
from app.utils import get_hashed_password, verify_password

session = create_session()

router = APIRouter(prefix='/auth', tags=['Авторизация'])

config = AuthXConfig(
    JWT_ALGORITHM=os.getenv('JWT_ALGORITHM', default='HS256'),
    JWT_SECRET_KEY=os.getenv(
        'JWT_SECRET_KEY', default=secrets.token_urlsafe(50),
    ),
    JWT_TOKEN_LOCATION=['cookies']

)

auth = AuthX(config=config)

app.add_middleware(
    MiddlewareOauth2,
    providers={
        'yandex': {
            'keys': 
        }
    }
)


@router.post('/register')
async def register(data: User):

    if await user_exists(data['email']):
        return HTTPException(400, detail='User already exists')

    user = User(
        email=data['email'],
        password=get_hashed_password(data['password'])
    )

    session.add(user)
    session.commit

    return user


@router.post('/login')
async def login(data: OAuth2PasswordRequestForm):
    email = data['email']

    user_email = (
        select(User.email)
        .where(User.email == email)
        .scalar_subquery()
    )

    password_inDB = (
            select(User.password)
            .where(User.email == email)
            .scalar_subquery()
        )

    if await user_exists():
        user_id = await session.execute(user_email)

        if data['email'] == user_email and verify_password(data['password'], password_inDB):

            user_id = await session.execute(user_email)
            token = auth.create_access_token(id=user_id)
            return {'access_token': token}

        raise HTTPException(401, detail={'message': 'Invalid password'})

    raise HTTPException(404, detail={'message': 'User does not exist'})


@router.post(
    '/refresh', dependencies=[Depends(auth.access_token_required)],
    status_code=status.HTTP_201_CREATED
)
async def refresh_token(request: Request, refresh_data):
    try:
        try:
            refresh_payload = await auth.refresh_token_required(request)
        except Exception as header_error:
            if not refresh_data or not refresh_data.refresh_token:
                raise header_error

            token = refresh_data.refresh_token
            refresh_payload = auth.verify_token(
                token,
                verify_type=True,
                type="refresh"
            )
        access_token = auth.create_access_token(refresh_payload.sub)
        return {"access_token": access_token}

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))