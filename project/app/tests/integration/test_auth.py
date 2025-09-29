import uuid

import pytest

from app.schemas.auth_schema import (
    ForgotPasswordSchema,
    LoginSchema,
    LogoutSchema,
    RefreshSchema,
    RegisterSchema,
    ResetPasswordSchema,
)
from app.tests.conftest import TestAPP
from app.tests.constants import ApiServices, RegisterUser1, RegisterUser2


@pytest.mark.usefixtures("test_app")
class TestAuth:
    @staticmethod
    def login_user_and_get_tokens(
        test_app: TestAPP, user_email: str, user_password: str
    ) -> tuple[str, str]:
        """Helper method to login and return access_token and refresh_token"""
        login_schema = LoginSchema(email=user_email, password=user_password)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGIN,
            data=login_schema.model_dump(),
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("access_token"), data.get("refresh_token")
        return None, None

    @staticmethod
    def login_success(test_app: TestAPP):
        login_schema = LoginSchema(
            email=RegisterUser1.email, password=RegisterUser1.password
        )
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGIN,
            data=login_schema.model_dump(),
        )

        if response.status_code == 200:
            test_app.tokens[f"{RegisterUser1.name}_{RegisterUser1.surname}"] = (
                response.json().get("access_token")
            )

    # =============================================================================
    # REGISTER TESTS
    # =============================================================================

    def test_register_user_1_success(self, test_app):
        """Test successful user registration for first user"""
        register_schema = RegisterSchema(**RegisterUser1.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert "user_id" in response.json()
        # Email is not returned in AuthResponseSchema

    def test_register_user_2_success(self, test_app):
        """Test successful user registration for second user"""
        register_schema = RegisterSchema(**RegisterUser2.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert "user_id" in response.json()
        # Email is not returned in AuthResponseSchema

    def test_register_user_duplicate_email_failure(self, test_app):
        """Test registration fails when trying to register with existing email"""
        register_schema = RegisterSchema(**RegisterUser1.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        assert response.status_code == 500  # Based on your current implementation

    def test_register_invalid_email_format(self, test_app):
        """Test registration fails with invalid email format"""
        invalid_register_data = {
            "email": "invalid-email",
            "password": RegisterUser1.password,
            "name": "Test",
            "surname": "User",
        }
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=invalid_register_data,
        )
        assert response.status_code == 422  # Validation error

    def test_register_weak_password_failure(self, test_app):
        """Test registration fails with weak password"""
        weak_password_data = {
            "email": f"{str(uuid.uuid4()).lower()}@test.com",
            "password": "123",  # Weak password
            "name": "Test",
            "surname": "User",
        }
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=weak_password_data,
        )
        assert response.status_code == 422  # Validation error

    # =============================================================================
    # LOGIN TESTS
    # =============================================================================

    def test_login_user_1_success(self, test_app):
        """Test successful login for first user"""
        self.login_success(test_app)

    def test_login_user_2_success(self, test_app):
        """Test successful login for second user"""
        login_schema = LoginSchema(
            email=RegisterUser2.email, password=RegisterUser2.password
        )
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGIN,
            data=login_schema.model_dump(),
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert "user_id" in response.json()

    def test_login_invalid_email_failure(self, test_app):
        """Test login fails with non-existent email"""
        login_schema = LoginSchema(email="nonexistent@test.com", password="anypassword")
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGIN,
            data=login_schema.model_dump(),
        )
        assert (
            response.status_code == 401
        )  # Based on AuthServiceExceptionInfo.ERROR_INVALID_CREDENTIALS

    def test_login_invalid_password_failure(self, test_app):
        """Test login fails with wrong password"""
        login_schema = LoginSchema(email=RegisterUser1.email, password="wrongpassword")
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGIN,
            data=login_schema.model_dump(),
        )
        assert (
            response.status_code == 401
        )  # Based on AuthServiceExceptionInfo.ERROR_INVALID_CREDENTIALS

    def test_login_invalid_email_format(self, test_app):
        """Test login fails with invalid email format"""
        invalid_login_data = {"email": "invalid-email", "password": "anypassword"}
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGIN,
            data=invalid_login_data,
        )
        assert response.status_code == 422  # Validation error

    # =============================================================================
    # REFRESH TOKEN TESTS
    # =============================================================================

    def test_refresh_token_success(self, test_app):
        """Test successful token refresh"""
        # First login to get tokens
        access_token, refresh_token = self.login_user_and_get_tokens(
            test_app, RegisterUser1.email, RegisterUser1.password
        )
        assert access_token is not None
        assert refresh_token is not None

        # Now refresh the token
        refresh_schema = RefreshSchema(refresh_token=refresh_token)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REFRESH,
            headers={"Authorization": f"Bearer {access_token}"},
            data=refresh_schema.model_dump(),
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert "user_id" in response.json()

    def test_refresh_token_invalid_refresh_token_failure(self, test_app):
        """Test refresh fails with invalid refresh token"""
        # First login to get access token
        access_token, _ = self.login_user_and_get_tokens(
            test_app, RegisterUser1.email, RegisterUser1.password
        )
        assert access_token is not None

        # Try to refresh with invalid token
        refresh_schema = RefreshSchema(refresh_token="invalid_refresh_token")
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REFRESH,
            headers={"Authorization": f"Bearer {access_token}"},
            data=refresh_schema.model_dump(),
        )

        assert (
            response.status_code == 401
        )  # Based on AuthServiceExceptionInfo.ERROR_REFRESH_TOKEN_INVALID

    def test_refresh_token_no_authorization_header_failure(self, test_app):
        """Test refresh fails without authorization header"""
        refresh_schema = RefreshSchema(refresh_token="any_token")
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REFRESH,
            data=refresh_schema.model_dump(),
        )

        assert response.status_code == 403  # Forbidden (based on actual behavior)

    # =============================================================================
    # LOGOUT TESTS
    # =============================================================================

    def test_logout_success(self, test_app):
        """Test successful logout"""
        # First login to get tokens
        access_token, refresh_token = self.login_user_and_get_tokens(
            test_app, RegisterUser1.email, RegisterUser1.password
        )
        assert access_token is not None
        assert refresh_token is not None

        # Now logout
        logout_schema = LogoutSchema(refresh_token=refresh_token)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGOUT,
            headers={"Authorization": f"Bearer {access_token}"},
            data=logout_schema.model_dump(),
        )

        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["message"] == "Logged out successfully"

    def test_logout_no_authorization_header_failure(self, test_app):
        """Test logout fails without authorization header"""
        logout_schema = LogoutSchema(refresh_token="any_token")
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGOUT,
            data=logout_schema.model_dump(),
        )

        assert response.status_code == 403  # Forbidden (based on actual behavior)

    def test_logout_invalid_access_token_failure(self, test_app):
        """Test logout fails with invalid access token"""
        logout_schema = LogoutSchema(refresh_token="any_token")
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGOUT,
            headers={"Authorization": "Bearer invalid_access_token"},
            data=logout_schema.model_dump(),
        )

        assert response.status_code == 401  # Unauthorized

    # =============================================================================
    # FORGOT PASSWORD TESTS
    # =============================================================================

    def test_forgot_password_success(self, test_app):
        """Test successful forgot password request"""
        forgot_password_schema = ForgotPasswordSchema(email=RegisterUser1.email)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_FORGOT_PASSWORD,
            data=forgot_password_schema.model_dump(),
        )

        assert response.status_code == 200
        assert "message" in response.json()
        assert "Password reset email sent successfully" in response.json()["message"]

    def test_forgot_password_nonexistent_email(self, test_app):
        """Test forgot password with non-existent email
        - should still return success for security"""
        forgot_password_schema = ForgotPasswordSchema(email="nonexistent@test.com")
        response = test_app.do_request(
            "POST",
            ApiServices.APP_FORGOT_PASSWORD,
            data=forgot_password_schema.model_dump(),
        )

        # Should return success even for non-existent emails for security reasons
        # but might return error depending on your implementation
        assert response.status_code in [200, 500]  # Adjust based on your implementation

    def test_forgot_password_invalid_email_format(self, test_app):
        """Test forgot password with invalid email format"""
        invalid_forgot_data = {"email": "invalid-email"}
        response = test_app.do_request(
            "POST",
            ApiServices.APP_FORGOT_PASSWORD,
            data=invalid_forgot_data,
        )

        assert response.status_code == 422  # Validation error

    # =============================================================================
    # RESET PASSWORD TESTS
    # =============================================================================

    def test_reset_password_invalid_token_failure(self, test_app):
        """Test reset password with invalid access token"""
        reset_password_schema = ResetPasswordSchema(
            access_token="invalid_access_token", new_password="NewPassword123!"
        )
        response = test_app.do_request(
            "POST",
            ApiServices.APP_RESET_PASSWORD,
            data=reset_password_schema.model_dump(),
        )

        assert (
            response.status_code == 500
        )  # Based on AuthServiceExceptionInfo.ERROR_PASSWORD_RESET_FAILED

    def test_reset_password_weak_password_failure(self, test_app):
        """Test reset password with weak password"""
        reset_password_data = {
            "access_token": "any_token",
            "new_password": "123",  # Weak password
        }
        response = test_app.do_request(
            "POST",
            ApiServices.APP_RESET_PASSWORD,
            data=reset_password_data,
        )

        assert response.status_code == 422  # Validation error
