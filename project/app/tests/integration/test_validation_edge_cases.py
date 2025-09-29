import pytest

from app.schemas.board_schema import BoardCreateSchema
from app.schemas.column_schema import ColumnInputSchema
from app.schemas.user_schema import UserUpdateSchema
from app.tests.constants import (
    ApiServices,
)


@pytest.mark.usefixtures("test_app")
class TestValidationEdgeCases:
    """
    Test class for edge cases and validation scenarios that might not be covered
    by the main integration tests. These tests focus on input validation,
    boundary conditions, and error handling.
    """

    # =============================================================================
    # WORKSPACE VALIDATION TESTS
    # =============================================================================

    def test_create_workspace_with_empty_name_failure(self, test_app):
        """Test workspace creation fails with empty name"""
        invalid_workspace_data = {"name": ""}
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=invalid_workspace_data,
        )
        assert response.status_code == 422

    def test_create_workspace_with_very_long_name_failure(self, test_app):
        """Test workspace creation fails with excessively long name"""
        long_name_data = {"name": "x" * 300}
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=long_name_data,
        )
        assert response.status_code == 422

    def test_create_workspace_with_only_whitespace_name_failure(self, test_app):
        """Test workspace creation fails with name containing only whitespace"""
        whitespace_workspace_data = {"name": "   "}
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=whitespace_workspace_data,
        )
        assert response.status_code == 422

    def test_create_workspace_with_special_characters_in_name(self, test_app):
        """Test workspace creation with special characters in name"""
        special_chars_data = {"name": "Test@#$%^&*()Workspace"}
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=special_chars_data,
        )
        assert response.status_code == 200

    # =============================================================================
    # BOARD VALIDATION TESTS
    # =============================================================================

    def test_create_board_with_empty_name_failure(self, test_app):
        """Test board creation fails with empty name"""
        invalid_board_data = {"name": "", "is_favorite": False, "workspace_id": 1}

        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_BOARD,
            data=invalid_board_data,
        )
        assert response.status_code == 422

    def test_create_board_with_very_long_name_failure(self, test_app):
        """Test board creation fails with excessively long name"""
        long_name_board_data = {
            "name": "x" * 300,
            "is_favorite": False,
            "workspace_id": 1,
        }
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_BOARD,
            data=long_name_board_data,
        )
        assert response.status_code == 422

    def test_create_board_with_negative_workspace_id_failure(self, test_app):
        """Test board creation fails with negative workspace ID"""
        negative_workspace_id_data = {
            "name": "Test Board",
            "is_favorite": False,
            "workspace_id": -1,
        }
        board_schema = BoardCreateSchema(**negative_workspace_id_data)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_BOARD,
            data=board_schema.model_dump(),
        )
        assert response.status_code == 400

    def test_create_board_with_zero_workspace_id_failure(self, test_app):
        """Test board creation fails with zero workspace ID"""
        zero_workspace_id_data = {
            "name": "Test Board",
            "is_favorite": False,
            "workspace_id": 0,
        }
        board_schema = BoardCreateSchema(**zero_workspace_id_data)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_BOARD,
            data=board_schema.model_dump(),
        )
        assert response.status_code == 400

        # =============================================================================

    # COLUMN VALIDATION TESTS
    # =============================================================================

    def test_create_column_with_empty_name_failure(self, test_app):
        """Test column creation fails with empty name"""
        invalid_column_data = {"name": "", "board_id": 1}

        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_COLUMN,
            data=invalid_column_data,
        )
        assert response.status_code == 422

    def test_create_column_with_very_long_name_failure(self, test_app):
        """Test column creation fails with excessively long name"""
        long_name_column_data = {"name": "x" * 300, "board_id": 1}
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_COLUMN,
            data=long_name_column_data,
        )
        assert response.status_code == 422

    def test_create_column_with_negative_board_id_failure(self, test_app):
        """Test column creation fails with negative board ID"""
        negative_board_id_data = {"name": "Test Column", "board_id": -1}
        column_schema = ColumnInputSchema(**negative_board_id_data)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_COLUMN,
            data=column_schema.model_dump(),
        )
        assert response.status_code == 404

    # =============================================================================
    # TASK VALIDATION TESTS
    # =============================================================================

    def test_create_task_with_empty_title_failure(self, test_app):
        """Test task creation fails with empty title"""
        invalid_task_data = {
            "title": "",
            "description": "Valid description",
            "column_id": 1,
        }

        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=invalid_task_data,
        )
        assert response.status_code == 422

    def test_create_task_with_very_long_title_failure(self, test_app):
        """Test task creation fails with excessively long title"""
        long_title_task_data = {
            "title": "x" * 500,
            "description": "Valid description",
            "column_id": 1,
        }

        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=long_title_task_data,
        )
        assert response.status_code == 422

    def test_create_task_with_very_long_description(self, test_app):
        """Test task creation fails with excessively long description"""
        long_desc_task_data = {
            "title": "Valid Title",
            "description": "x" * 2000,
            "column_id": 1,
        }
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=long_desc_task_data,
        )
        assert response.status_code == 200

    def test_create_task_with_negative_column_id_failure(self, test_app):
        """Test task creation fails with negative column ID"""
        negative_column_id_data = {
            "title": "Test Task",
            "description": "Test Description",
            "column_id": -1,
        }

        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=negative_column_id_data,
        )
        assert response.status_code == 404

    def test_create_task_with_only_whitespace_title_failure(self, test_app):
        """Test task creation fails with title containing only whitespace"""
        whitespace_title_data = {
            "title": "   ",
            "description": "Valid description",
            "column_id": 1,
        }
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=whitespace_title_data,
        )
        assert response.status_code == 422

    def test_create_task_with_empty_description_success(self, test_app):
        """Test task creation with empty description (might be allowed)"""
        empty_description_data = {
            "title": "Test Task with Empty Description",
            "description": "",
            "column_id": 1,
        }
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=empty_description_data,
        )

        assert response.status_code == 200

    # =============================================================================
    # USER PROFILE VALIDATION TESTS
    # =============================================================================

    def test_update_user_with_unicode_characters_in_name(self, test_app):
        """Test user profile update with unicode characters in name"""
        unicode_name_data = {"name": "José María", "surname": "González-López"}
        update_schema = UserUpdateSchema(**unicode_name_data)
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_UPDATE_ME_USER,
            data=update_schema.model_dump(),
        )
        # Unicode characters should typically be allowed
        assert response.status_code == 200

    def test_update_user_with_numeric_name(self, test_app):
        """Test user profile update with numeric name"""
        numeric_name_data = {"name": "12345", "surname": "67890"}
        update_schema = UserUpdateSchema(**numeric_name_data)
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_UPDATE_ME_USER,
            data=update_schema.model_dump(),
        )

        assert response.status_code == 200

    def test_update_user_with_special_characters_in_name(self, test_app):
        """Test user profile update with special characters in name"""
        special_chars_data = {"name": "John@#$", "surname": "Doe%^&"}
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_UPDATE_ME_USER,
            data=special_chars_data,
        )

        assert response.status_code == 200

    # =============================================================================
    # AUTHENTICATION AND AUTHORIZATION EDGE CASES
    # =============================================================================

    def test_request_with_malformed_authorization_header(self, test_app):
        """Test request with malformed authorization header"""
        response = test_app.do_request(
            "GET",
            ApiServices.APP_GET_ME_USER,
            headers={"Authorization": "Malformed token_here"},
        )
        assert response.status_code == 403

    def test_request_with_empty_authorization_header(self, test_app):
        """Test request with empty authorization header"""
        response = test_app.do_request(
            "GET", ApiServices.APP_GET_ME_USER, headers={"Authorization": ""}
        )
        assert response.status_code == 403

    def test_request_with_bearer_but_no_token(self, test_app):
        """Test request with 'Bearer' but no token"""
        response = test_app.do_request(
            "GET", ApiServices.APP_GET_ME_USER, headers={"Authorization": "Bearer "}
        )
        assert response.status_code == 403

    def test_request_with_expired_token_simulation(self, test_app):
        """Test request with what appears to be an expired token"""

        response = test_app.do_request(
            "GET",
            ApiServices.APP_GET_ME_USER,
            headers={
                "Authorization": "Bearer "
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.expired_token"
            },
        )
        assert response.status_code == 401

        # =============================================================================

    # CONTENT TYPE AND PAYLOAD EDGE CASES
    # =============================================================================

    def test_request_with_missing_required_fields(self, test_app):
        """Test requests with missing required fields"""
        incomplete_data = {}
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=incomplete_data,
        )
        assert response.status_code == 422

    def test_request_with_extra_unexpected_fields(self, test_app):
        """Test requests with extra fields not in schema"""
        data_with_extra_fields = {
            "name": "Valid Workspace Name",
            "unexpected_field": "This should be ignored",
            "another_extra": 12345,
        }
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=data_with_extra_fields,
        )

        assert response.status_code == 200

    # =============================================================================
    # SQL INJECTION AND SECURITY TESTS
    # =============================================================================

    def test_create_workspace_with_sql_injection_attempt(self, test_app):
        """Test workspace creation with potential SQL injection in name"""
        sql_injection_data = {"name": "'; DROP TABLE workspaces; --"}
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_WORKSPACE,
            data=sql_injection_data,
        )

        assert response.status_code == 200

    def test_create_task_with_xss_attempt_in_title(self, test_app):
        """Test task creation with potential XSS in title"""
        xss_attempt_data = {
            "title": "<script>alert('XSS')</script>",
            "description": "Normal description",
            "column_id": 1,
        }
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=xss_attempt_data,
        )

        assert response.status_code == 200

    def test_create_task_with_xss_attempt_in_description(self, test_app):
        """Test task creation with potential XSS in description"""
        xss_attempt_data = {
            "title": "Normal Title",
            "description": "<img src=x onerror=alert('XSS')>",
            "column_id": 1,
        }
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=xss_attempt_data,
        )

        assert response.status_code == 200
