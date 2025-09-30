import pytest
from requests import Response

from app.schemas.board_schema import (
    BoardCreateSchema,
    BoardInvitationSchema,
    BoardOutputSchema,
    BoardRemoveMemberSchema,
    BoardUpdateSchema,
)
from app.tests.conftest import TestAPP
from app.tests.constants import (
    ApiServices,
    BoardCreate,
    BoardInviteUser,
    BoardRemoveUser,
    BoardRemoveUserErrorOwner,
    BoardUpdate,
)


@pytest.mark.usefixtures("test_app")
class TestBoard:
    @staticmethod
    def invitation_user_board(
        board_invite_schema: BoardInvitationSchema, test_app: TestAPP
    ) -> Response:
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_BOARD_INVITE_USER,
            data=board_invite_schema.model_dump(),
        )
        return response

    @staticmethod
    def remove_user_board(
        board_remove_user_schema: BoardRemoveMemberSchema, test_app: TestAPP
    ) -> Response:
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_BOARD_REMOVE_USER,
            data=board_remove_user_schema.model_dump(),
        )
        return response

    def test_get_all_board_paginated_none_board(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_BOARD_GET_ALL.format(workspace_id=test_app.workspace_1.id),
        )
        assert response.status_code == 200

    def test_create_board(self, test_app):
        board_schema = BoardCreateSchema(**BoardCreate.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_BOARD,
            data=board_schema.model_dump(),
        )

        assert response.status_code == 200
        test_app.board_1 = BoardOutputSchema(**response.json())

    def test_create_board_2(self, test_app):
        board_schema = BoardCreateSchema(**BoardCreate.__dict__)
        board_schema.name = "Board 2"
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_BOARD,
            data=board_schema.model_dump(),
        )

        assert response.status_code == 200
        test_app.board_2 = BoardOutputSchema(**response.json())

    def test_get_all_board_paginated_with_board(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_BOARD_GET_ALL.format(workspace_id=test_app.workspace_1.id),
        )
        assert response.status_code == 200

    def test_get_all_board_favorites_paginated_none_board(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_BOARD_GET_ALL.format(workspace_id=test_app.workspace_1.id),
            data={"is_favourite": True},
        )
        assert response.status_code == 200

    def test_update_board_favorite(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_BOARD_UPDATE_FAVORITE.format(board_id=test_app.board_1.id),
        )
        assert response.status_code == 200
        test_app.board_1 = BoardOutputSchema(**response.json())

    def test_get_all_board_favorites_paginated_with_board(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_BOARD_GET_ALL.format(workspace_id=test_app.workspace_1.id),
            data={"is_favourite": True},
        )
        assert response.status_code == 200

    def test_invite_user_board(self, test_app):
        board_invite_schema = BoardInvitationSchema(**BoardInviteUser.__dict__)
        response = self.invitation_user_board(board_invite_schema, test_app)
        assert response.status_code == 200

    def test_invite_user_board_exist(self, test_app):
        board_invite_schema = BoardInvitationSchema(**BoardInviteUser.__dict__)
        response = self.invitation_user_board(board_invite_schema, test_app)
        assert response.status_code == 400

    def test_remove_user_board(self, test_app):
        board_remove_user_schema = BoardRemoveMemberSchema(**BoardRemoveUser.__dict__)
        response = self.remove_user_board(board_remove_user_schema, test_app)
        print(response.json())
        assert response.status_code == 200

    def test_remove_user_board_none_contains(self, test_app):
        board_remove_user_schema = BoardRemoveMemberSchema(**BoardRemoveUser.__dict__)
        response = self.remove_user_board(board_remove_user_schema, test_app)
        print(response.json())
        assert response.status_code == 400

    def test_remove_user_board_error_owner(self, test_app):
        board_remove_user_schema = BoardRemoveMemberSchema(
            **BoardRemoveUserErrorOwner.__dict__
        )
        response = self.remove_user_board(board_remove_user_schema, test_app)
        assert response.status_code == 403

    def test_board_get_members(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_BOARD_GET_MEMBERS.format(board_id=test_app.board_1.id),
        )
        assert response.status_code == 200

    def test_delete_board_none_owner(self, test_app):
        response = test_app.do_request_with_role(
            "USER_2",
            "DELETE",
            ApiServices.APP_BOARD_REMOVE.format(board_id=test_app.board_2.id),
        )
        assert response.status_code == 403

    def test_update_name_board_none_owner(self, test_app):
        board_update_schema = BoardUpdateSchema(**BoardUpdate.__dict__)

        response = test_app.do_request_with_role(
            "USER_2",
            "PUT",
            ApiServices.APP_BOARD_UPDATE.format(board_id=test_app.board_1.id),
            data=board_update_schema.model_dump(),
        )

        assert response.status_code == 403

    def test_update_name_board_success(self, test_app):
        board_update_schema = BoardUpdateSchema(**BoardUpdate.__dict__)

        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_BOARD_UPDATE.format(board_id=test_app.board_1.id),
            data=board_update_schema.model_dump(),
        )

        assert response.status_code == 200
        test_app.board_1 = BoardOutputSchema(**response.json())

    def test_update_name_with_same_board_name(self, test_app):
        board_update_schema = BoardUpdateSchema(name=test_app.board_1.name)

        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_BOARD_UPDATE.format(board_id=test_app.board_2.id),
            data=board_update_schema.model_dump(),
        )

        assert response.status_code == 400

    def test_update_name_with_my_same_board_name(self, test_app):
        board_update_schema = BoardUpdateSchema(name=test_app.board_1.name)

        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_BOARD_UPDATE.format(board_id=test_app.board_1.id),
            data=board_update_schema.model_dump(),
        )

        assert response.status_code == 200

    def test_delete_board_success(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_BOARD_REMOVE.format(board_id=test_app.board_2.id),
        )
        assert response.status_code == 200

    def test_delete_board_none_exist(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_BOARD_REMOVE.format(board_id=test_app.board_2.id),
        )
        assert response.status_code == 404

    def test_update_name_with_board_none_exist(self, test_app):
        board_update_schema = BoardUpdateSchema(name=test_app.board_1.name)

        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_BOARD_UPDATE.format(board_id=test_app.board_2.id),
            data=board_update_schema.model_dump(),
        )
        print(response.json())
        assert response.status_code == 404
