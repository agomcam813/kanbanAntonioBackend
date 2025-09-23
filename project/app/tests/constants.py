import uuid
from typing import Final

email_random_1 = f"{str(uuid.uuid4()).lower()}@gmail.com"
email_random_2 = f"{str(uuid.uuid4()).lower()}@gmail.com"

password_random_1 = f"{uuid.uuid4()}A?"

class ApiServices:
    # AUTH
    APP_REGISTER: Final[str] = "/auth/register"
    APP_LOGIN: Final[str] = "/auth/login"

    # USER
    APP_DELETE_ME_USER: Final[str] = "/users/me"
    APP_UPDATE_ME_USER: Final[str] = "/users/me"
    APP_GET_ME_USER: Final[str] = "/users/me"

    # WORKSPACE
    APP_WORKSPACES: Final[str] = "/workspaces"
    APP_WORKSPACE: Final[str] = "/workspaces/{workspace_id}"
    APP_WORKSPACE_USERS: Final[str] = "/workspaces/{workspace_id}/users"
    APP_WORKSPACE_USER: Final[str] = "/workspaces/{workspace_id}/users/{user_id}"

    # BOARD
    APP_BOARDS: Final[str] = "/workspaces/{workspace_id}/boards"
    APP_BOARD: Final[str] = "/workspaces/{workspace_id}/boards/{board_id}"
    APP_BOARD_USERS: Final[str] = "/workspaces/{workspace_id}/boards/{board_id}/users"
    APP_BOARD_USER: Final[str] = (
        "/workspaces/{workspace_id}/boards/{board_id}/users/{user_id}"
    )

    # COLUMN
    APP_COLUMNS: Final[str] = "/workspaces/{workspace_id}/boards/{board_id}/columns"
    APP_COLUMN: Final[str] = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}"
    )
    APP_COLUMN_REORDER: Final[str] = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/reorder"
    )

    # TASK
    APP_TASKS: Final[str] = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}/tasks"
    )
    APP_TASK: Final[str] = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}/tasks/{task_id}"
    )
    APP_TASK_MOVE: Final[str] = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}/"
        "tasks/{task_id}/move"
    )


class Credentials:
    CREDENTIALS: Final[dict[str, dict[str, str]]] = {
        "USER_1": {
            "email": email_random_1,
            "password": password_random_1,
        },
    }


class RegisterUser1:
    email: Final[str] = email_random_1
    password: Final[str] = password_random_1
    name: Final[str] = "USER"
    surname: Final[str] = "1"


class UpdateUser1:
    name: str = "Name change"
    surname: str = "Surname change"


class TestWorkspace:
    name: Final[str] = "Test Workspace"
    description: Final[str] = "A workspace for testing purposes"
    updated_name: Final[str] = "Updated Test Workspace"
    updated_description: Final[str] = "Updated workspace description"


class Board1:
    name: Final[str] = "Test Board"
    description: Final[str] = "A board for testing purposes"
    updated_name: Final[str] = "Updated Test Board"
    updated_description: Final[str] = "Updated board description"


class TestColumn:
    name: Final[str] = "Test Column"
    order: Final[int] = 1
    updated_name: Final[str] = "Updated Test Column"
    updated_order: Final[int] = 2


class TestTask:
    title: Final[str] = "Test Task"
    description: Final[str] = "A task for testing purposes"
    order: Final[int] = 1
    updated_title: Final[str] = "Updated Test Task"
    updated_description: Final[str] = "Updated task description"
    updated_order: Final[int] = 2
