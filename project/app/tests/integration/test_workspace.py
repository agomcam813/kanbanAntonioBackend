import pytest

from app.modules.database_module.models.default import Workspace
from app.schemas.workspace_schema import WorkspaceInputSchema, WorkspaceInvitationSchema
from app.tests.constants import TestWorkspace1, ApiServices, WorkspaceInvitation


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
            ApiServices.APP_WORKSPACE_MEMBERS.format(workspace_id=test_app.workspace_1.id),
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
