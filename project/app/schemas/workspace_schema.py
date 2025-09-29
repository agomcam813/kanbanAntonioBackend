from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints

from app.schemas.base_schema import BaseSchema

NonEmptyStr = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True, max_length=255)
]


class WorkspaceInputSchema(BaseSchema):
    name: NonEmptyStr


class WorkspaceCreateSchema(WorkspaceInputSchema):
    owner_id: int


class WorkspaceOutputSchema(WorkspaceInputSchema):
    id: int
    owner_id: int = None
    created_at: datetime
    updated_at: datetime


class WorkspaceFilterByUserInputSchema(BaseSchema):
    workspace_id: int
    user_id: int


class WorkspaceFilterByUserIdOutputSchema(WorkspaceInputSchema):
    id: int


class WorkspaceInvitationSchema(BaseSchema):
    workspace_id: int
    invited_user_email: NonEmptyStr


class WorkspaceRemoveMemberSchema(BaseSchema):
    workspace_id: int
    user_email_to_remove: NonEmptyStr


class WorkspaceMemberOutputSchema(BaseSchema):
    id: int
    name: str
    surname: str
    email: str
    is_owner: bool
