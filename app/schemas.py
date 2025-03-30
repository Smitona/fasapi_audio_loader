from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        rom_attributes = True


class TokenData(BaseModel):
    refresh_token: str


class AudioResponse(BaseModel):
    name: str
    path: str


class FilePathRequest(BaseModel):
    file_path: str