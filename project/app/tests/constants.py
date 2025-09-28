import uuid
from typing import Final

from pydantic import EmailStr

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
    APP_BOARD: str = "/boards"
    APP_BOARD_GET_ALL: str = "/boards/all-board-paginated/{workspace_id}"
    APP_BOARD_UPDATE_FAVORITE: str = "/boards/update-favorite/{board_id}"
    APP_BOARD_INVITE_USER: str = "/boards/invite"
    APP_BOARD_REMOVE_USER: str = "/boards/remove-member"
    APP_BOARD_GET_MEMBERS: str = "/boards/{board_id}/members"

    # COLUMN
    APP_COLUMN: str = "/columns"
    APP_COLUMN_GET_ALL: str = "/columns/{board_id}"
    APP_COLUMN_CHANGE_NAME: str = "/columns/change-name"
    APP_COLUMN_MOVE: str = "/columns/move"
    APP_COLUMN_REMOVE: str = "/columns/{column_id}"

    # TASK
    APP_TASK: str = "/tasks/"


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


class TestWorkspace2:
    name: str = "Test Workspace 2"


class WorkspaceInvitation:
    workspace_id: int = 1
    invited_user_email: str = email_random_2


class WorkspaceRemoveInvitation:
    workspace_id: int = 1
    user_email_to_remove: str = email_random_2


class WorkspaceRemoveInvitationOwner:
    workspace_id: int = 1
    user_email_to_remove: str = email_random_1


class BoardCreate:
    name: str = "Test Board"
    is_favorite: bool = False
    workspace_id: int = 1


class BoardCreateErrorWorkspaceId:
    name: str = "Test Board"
    is_favorite: bool = False
    workspace_id: int = 1


class BoardInviteUser:
    board_id: int = 1
    invited_user_email: EmailStr = email_random_2


class BoardRemoveUser:
    board_id: int = 1
    user_email_to_remove: str = email_random_2


class BoardRemoveUserErrorOwner:
    board_id: int = 1
    user_email_to_remove: str = email_random_1


class ColumnCreate1:
    name: str = "Test Column"
    board_id: int = 1


class ColumnCreate2:
    name: str = "Test Column 2"
    board_id: int = 1


class ColumnChangeSameName:
    id: int = 1
    new_name: str = "Test Column"


class ColumnChangeDifferentName:
    id: int = 1
    new_name: str = str(uuid.uuid4()).lower()


class ColumnMove:
    id: int = 1
    new_order: int = 2

class TaskCreate:
    title: str = "Test Task"
    description: str = "Test Task Description"
    column_id: int = 1