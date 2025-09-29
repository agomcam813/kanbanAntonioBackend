from datetime import datetime
from typing import Annotated

from pydantic import Field, StringConstraints

from app.schemas.base_schema import BaseSchema

NonEmptyStr = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True, max_length=255)
]


# Input schema (user does not provide order)
class TaskInputSchema(BaseSchema):
    title: NonEmptyStr
    description: str
    column_id: int


# Create schema (service adds order)
class TaskCreateSchema(TaskInputSchema):
    order: int


# Output schema
class TaskOutputSchema(TaskCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskFilterByTitleAndBoard(BaseSchema):
    title: str
    board_id: int


class TaskUpdateOrderSchema(BaseSchema):
    id: int
    new_order: int = Field(gt=0)
    column_id: int


class TaskUpdateSchema(BaseSchema):
    id: int
    title: str
    description: str
