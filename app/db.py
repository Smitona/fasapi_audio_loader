from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, exists

from fasapi_audio_loader.app.models import User

Base = DeclarativeBase()

engine = create_async_engine('sqlite+aiosqlite://database.db')

new_session = async_sessionmaker(engine, expire_on_commit=False, echo=True)


async def create_session():
    async with new_session() as session:
        yield session


async def user_exists(email: str):
    session = create_session()

    user_email = (
        select(User.email)
        .where(User.email == email)
        .scalar_subquery()
    )

    return session.query(
        exists().where(User.email == user_email)
    ).scalar()
