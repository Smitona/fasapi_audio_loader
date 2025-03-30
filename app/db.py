from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy import exists, select

from app.models import Base

engine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True)

new_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_session():
    async with new_session() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def user_exists(User, email: str):
    async with new_session() as session:
        result = await session.execute(
            exists().where(User.email == email)
        )
        return result.scalar()


async def get_user(User, param, session):
    if isinstance(param, int):
        user_query = select(User).where(User.id == param)
        result = await session.execute(user_query)
        user = result.scalars().first()
    else:
        user_query = select(User).where(User.email == param)
        result = await session.execute(user_query)
        user = result.scalars().first()

    return user
