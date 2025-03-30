from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.db import get_user, create_session
from app.config import auth

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def superuser_required(
    token_data: dict = Depends(auth.access_token_required),
    session: AsyncSession = Depends(create_session)
):
    user_id = token_data.get('sub')
    if not user_id:
        raise HTTPException(
            401, detail='Invalid authentication credentials'
        )

    current_user = await get_user(User, user_id, session)
    if not current_user:
        raise HTTPException(404, detail='User not found')

    if not current_user.is_superuser:
        raise HTTPException(
            403, detail='Only superusers can perform this action'
        )

    return current_user