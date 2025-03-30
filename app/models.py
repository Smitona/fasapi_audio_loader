from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)

    audios: Mapped[List['Audio']] = relationship(back_populates='owner')


class Audio(Base):
    __tablename__ = 'audios'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    owner: Mapped['User'] = relationship(back_populates='audios')

