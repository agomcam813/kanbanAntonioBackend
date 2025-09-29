from datetime import datetime
from typing import Annotated, Optional

from pydantic import StringConstraints

from app.schemas.base_schema import BaseSchema

NonEmptyStr = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True, max_length=255)
]


class BoardCreateSchema(BaseSchema):
    name: NonEmptyStr
    is_favorite: Optional[bool] = False
    workspace_id: int


class BoardOutputSchema(BoardCreateSchema):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class BoardFilterByNameSchema(BaseSchema):
    name: str
    workspace_id: int


class BoardUpdateSchema(BaseSchema):
    name: Optional[NonEmptyStr] = None


class BoardPaginateSchema(BaseSchema):
    data: list[BoardOutputSchema]
    total: int


class BoardFavoriteSchema(BaseSchema):
    board_id: int
    user_id: int


class BoardInvitationSchema(BaseSchema):
    board_id: int
    invited_user_email: str


class BoardRemoveMemberSchema(BaseSchema):
    board_id: int
    user_email_to_remove: str


class BoardMemberOutputSchema(BaseSchema):
    id: int
    name: str
    surname: str
    email: str
    is_owner: bool
