from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)

    audios: Mapped['Audio'] = relationship(back_populates='owner')


class Audio(Base):
    __tablename__ = 'audios'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    path: Mapped[str]
    owner: Mapped['User'] = relationship(back_populates='audios')
