from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserDataSourceConfigCreate(BaseModel):
    data_source_key: str
    is_enabled: bool = True
    is_paid: bool = False
    credentials: str
    config_json: str | None = None


class UserDataSourceConfig(UserDataSourceConfigCreate):
    id: int
    user_id: int
    data_source_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserInDB(User):
    password_hash: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class Resume(BaseModel):
    id: int
    filename: str
    storage_url: str
    parsed_json: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
