from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    password: str

    class Config:
        rom_attributes = True


class RefreshData(BaseModel):
    refresh_token: str
