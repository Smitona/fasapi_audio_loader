from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import exists

engine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True)

new_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


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
