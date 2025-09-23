import uuid
from typing import Final

email_random_1 = f"{str(uuid.uuid4()).lower()}@gmail.com"
email_random_2 = f"{str(uuid.uuid4()).lower()}@gmail.com"

password_random_1 = f"{uuid.uuid4()}A?"


class ApiServices:
    # AUTH
    APP_REGISTER: str = "/auth/register"
    APP_LOGIN: str = "/auth/login"

    # USER
    APP_DELETE_ME_USER: str = "/users/me"
    APP_UPDATE_ME_USER: str = "/users/me"
    APP_GET_ME_USER: str = "/users/me"

    # WORKSPACE
    APP_WORKSPACE: str = "/workspaces"
    APP_WORKSPACE_ME: str = "/workspaces/all-me"
    APP_WORKSPACE_MEMBERS: str = "/workspaces/{workspace_id}/members"
    APP_WORKSPACE_INVITE_MEMBERS: str = "/workspaces/invite"
    APP_WORKSPACE_REMOVE_INVITE_MEMBERS: str = "/workspaces/remove-member"
    APP_WORKSPACE_REMOVE: str = "/workspaces/remove-workspace/{workspace_id}"

    # BOARD
    APP_BOARDS: str = "/workspaces/{workspace_id}/boards"
    APP_BOARD: str = "/workspaces/{workspace_id}/boards/{board_id}"
    APP_BOARD_USERS: str = "/workspaces/{workspace_id}/boards/{board_id}/users"
    APP_BOARD_USER: str = "/workspaces/{workspace_id}/boards/{board_id}/users/{user_id}"

    # COLUMN
    APP_COLUMNS: str = "/workspaces/{workspace_id}/boards/{board_id}/columns"
    APP_COLUMN: str = "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}"
    APP_COLUMN_REORDER: str = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/reorder"
    )

    # TASK
    APP_TASKS: str = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}/tasks"
    )
    APP_TASK: str = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}"
        "/tasks/{task_id}"
    )
    APP_TASK_MOVE: str = (
        "/workspaces/{workspace_id}/boards/{board_id}/columns/{column_id}/"
        "tasks/{task_id}/move"
    )


class Credentials:
    CREDENTIALS: Final[dict[str, dict[str, str]]] = {
        "USER_1": {
            "email": email_random_1,
            "password": password_random_1,
        },
        "USER_2": {
            "email": email_random_2,
            "password": password_random_1,
        },
    }


class RegisterUser1:
    email: str = email_random_1
    password: str = password_random_1
    name: str = "USER"
    surname: str = "1"


class RegisterUser2:
    email: str = email_random_2
    password: str = password_random_1
    name: str = "USER"
    surname: str = "2"


class UpdateUser1:
    name: str = "Name change"
    surname: str = "Surname change"


class TestWorkspace1:
    name: str = "Test Workspace"


class WorkspaceInvitation:
    workspace_id: int = 1
    invited_user_email: str = email_random_2


class WorkspaceRemoveInvitation:
    workspace_id: int = 1
    user_email_to_remove: str = email_random_2


class WorkspaceRemoveInvitationOwner:
    workspace_id: int = 1
    user_email_to_remove: str = email_random_1
