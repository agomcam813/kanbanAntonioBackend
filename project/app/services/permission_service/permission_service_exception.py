from app.schemas.base_schema import BaseException, BaseExceptionInfo


class PermissionServiceExceptionInfo(BaseExceptionInfo):
    ERROR_USER_NOT_IN_WORKSPACE = (
        7001,
        "User does not have access to this workspace",
        403,
    )
    ERROR_BOARD_NOT_FOUND = (7002, "Board not found", 404)
    ERROR_COLUMN_NOT_FOUND = (7003, "Column not found", 404)
    ERROR_TASK_NOT_FOUND = (7004, "Task not found", 404)
    ERROR_WORKSPACE_NOT_FOUND = (7005, "Workspace not found", 404)
    ERROR_BOARD_NOT_IN_WORKSPACE = (7006, "Board does not belong to workspace", 403)
    ERROR_COLUMN_NOT_IN_BOARD = (7007, "Column does not belong to board", 403)
    ERROR_TASK_NOT_IN_COLUMN = (7008, "Task does not belong to column", 403)
    ERROR_USER_NOT_WORKSPACE_OWNER = (7009, "User is not the workspace owner", 403)
    ERROR_USER_NOT_BOARD_OWNER = (7010, "User is not the board owner", 403)
    ERROR_USER_NOT_IN_BOARD = (7011, "User does not belong to this board", 403)


class PermissionServiceException(BaseException):
    pass
