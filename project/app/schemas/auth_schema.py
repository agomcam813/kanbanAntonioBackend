from typing import Annotated, Any, Dict

from pydantic import BaseModel, EmailStr, StringConstraints, field_validator

from app.utils.string_helper import StringHelper

NonEmptyStr = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True, max_length=255)
]


class AuthDataOutputSchema(BaseModel):
    token: str
    payload: Dict[str, Any]


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: NonEmptyStr
    surname: NonEmptyStr

    @field_validator("password")
    def validate_password(v: str) -> str:
        return StringHelper.validate_password_complexity(v)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordSchema(BaseModel):
    access_token: str
    new_password: str

    @field_validator("new_password", mode="after")
    def validate_password(v: str) -> str:
        return StringHelper.validate_password_complexity(v)


class RefreshSchema(BaseModel):
    refresh_token: str


class LogoutSchema(BaseModel):
    refresh_token: str


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class AuthResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
