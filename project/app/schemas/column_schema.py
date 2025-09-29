from typing import Annotated

from pydantic import StringConstraints

from app.schemas.base_schema import BaseSchema
from app.schemas.task_schema import TaskOutputSchema

NonEmptyStr = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True, max_length=255)
]


# Input schema for creating a column (user does not provide order)
class ColumnInputSchema(BaseSchema):
    name: NonEmptyStr
    board_id: int


# Output schema (includes auto-generated order)
class ColumnOutputSchema(BaseSchema):
    id: int
    name: str
    order: int
    board_id: int


# Schema with tasks for board retrieval
class ColumnWithTasksSchema(ColumnOutputSchema):
    tasks: list[TaskOutputSchema]


# Helper schema for filtering by name and board
class ColumnFilterNameAndBoardIdSchema(BaseSchema):
    name: str
    board_id: int


class ColumnUpdateOrderSchema(BaseSchema):
    id: int
    new_order: int


class ColumnUpdateNameSchema(BaseSchema):
    id: int
    new_name: NonEmptyStr
