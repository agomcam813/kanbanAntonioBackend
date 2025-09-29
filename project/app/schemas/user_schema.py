from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints

NonEmptyStr = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True, max_length=255)
]


class UserInputSchema(BaseModel):
    name: NonEmptyStr
    surname: NonEmptyStr
    email: EmailStr


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None


class UserOutputSchema(UserInputSchema):
    id: int
    created_at: datetime
    updated_at: datetime
