import uuid

import pytest

from app.modules.database_module.models.default import Workspace
from app.schemas.workspace_schema import (
    WorkspaceInputSchema,
    WorkspaceInvitationSchema,
    WorkspaceRemoveMemberSchema,
)
from app.tests.constants import (
    ApiServices,
    TestWorkspace1,
    WorkspaceInvitation,
    WorkspaceRemoveInvitation,
    WorkspaceRemoveInvitationOwner,
)


@pytest.mark.usefixtures("test_app")
class TestWorkspace:

    def test_create_workspace_success(self, test_app):
        workspace_schema = WorkspaceInputSchema(**TestWorkspace1.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=workspace_schema.model_dump(),
        )
        assert response.status_code == 200
        assert response.json().get("name") == TestWorkspace1.name
        test_app.workspace_1 = Workspace(**response.json())

    def test_create_workspace_same_name(self, test_app):
        workspace_schema = WorkspaceInputSchema(**TestWorkspace1.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=workspace_schema.model_dump(),
        )
        assert response.status_code == 400

    def test_get_all_workspaces_me_success(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_WORKSPACE_ME,
        )
        assert response.status_code == 200

    def test_get_workspace_members_success(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_WORKSPACE_MEMBERS.format(
                workspace_id=test_app.workspace_1.id
            ),
        )

        assert response.status_code == 200

    def test_invite_workspace_members_success(self, test_app):
        invite_schema = WorkspaceInvitationSchema(**WorkspaceInvitation.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE_INVITE_MEMBERS,
            data=invite_schema.model_dump(),
        )

        assert response.status_code == 200

    def test_delete_workspace_member_success(self, test_app):
        invite_schema = WorkspaceRemoveMemberSchema(
            **WorkspaceRemoveInvitation.__dict__
        )
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_WORKSPACE_REMOVE_INVITE_MEMBERS,
            data=invite_schema.model_dump(),
        )

        assert response.status_code == 200

    def test_delete_workspace_member_not_exist(self, test_app):
        invite_schema = WorkspaceRemoveMemberSchema(
            **WorkspaceRemoveInvitation.__dict__
        )
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_WORKSPACE_REMOVE_INVITE_MEMBERS,
            data=invite_schema.model_dump(),
        )

        assert response.status_code == 400

    def test_delete_workspace_member_not_exist_user(self, test_app):
        invite_schema = WorkspaceRemoveMemberSchema(
            **WorkspaceRemoveInvitation.__dict__
        )
        invite_schema.user_email_to_remove = f"{str(uuid.uuid4()).lower()}@gmail.com"
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_WORKSPACE_REMOVE_INVITE_MEMBERS,
            data=invite_schema.model_dump(),
        )

        assert response.status_code == 404

    def test_delete_workspace_owner_member_exist(self, test_app):
        invite_schema = WorkspaceRemoveMemberSchema(
            **WorkspaceRemoveInvitationOwner.__dict__
        )
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_WORKSPACE_REMOVE_INVITE_MEMBERS,
            data=invite_schema.model_dump(),
        )

        assert response.status_code == 403

    def test_delete_workspace_fails_when_user_not_owner(self, test_app):
        response = test_app.do_request_with_role(
            "USER_2",
            "DELETE",
            ApiServices.APP_WORKSPACE_REMOVE.format(
                workspace_id=test_app.workspace_1.id
            ),
        )
        assert response.status_code == 403
