import os
from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import create_session, get_user
from app.schemas import AudioResponse
from app.models import Audio, User
from app.utils import auth

audio_route = APIRouter(prefix='/audio', tags=['Аудио'])


def validate_mp3(file: UploadFile = File(...)):
    if not file.filename.endswith('.mp3'):
        raise HTTPException(400, detail="Only MP3 files are allowed")

    if file.content_type not in ["audio/mpeg", "audio/mp3"]:
        raise HTTPException(400, detail="File content must be MP3 format")

    return file


@audio_route.get(
    '/', response_model=list[AudioResponse],
    status_code=status.HTTP_200_OK
)
async def list_users(
    session: AsyncSession = Depends(create_session)
):
    result = await session.execute(select(Audio))
    audios = result.scalars().all()
    return audios


@audio_route.post(
    '/add', response_model=list[AudioResponse],
    status_code=status.HTTP_201_CREATED
)
async def add_audio(
    name: str, file_path: str,
    file: UploadFile = Depends(validate_mp3),
    session: AsyncSession = Depends(auth.access_token_required),
    token_data: dict = Depends(auth.access_token_required)
):
    user_id = token_data.sub
    current_user = await get_user(User, user_id, session)

    audio = Audio(
        name=name,
        path=file_path,
        owner_id=user_id,
        owner=current_user
    )

    await session.add(audio)
    await session.commit()
    await session.refresh(audio)

    return audio