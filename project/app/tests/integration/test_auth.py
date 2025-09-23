import pytest

from app.schemas.auth_schema import LoginSchema, RegisterSchema
from app.tests.constants import ApiServices, RegisterUser1, RegisterUser2


@pytest.mark.usefixtures("test_app")
class TestAuth:
    def test_register_1_success(self, test_app):
        register_schema = RegisterSchema(**RegisterUser1.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        assert response.status_code == 200

    def test_register_2_success(self, test_app):
        register_schema = RegisterSchema(**RegisterUser2.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        assert response.status_code == 200

    def test_register_failure(self, test_app):
        register_schema = RegisterSchema(**RegisterUser1.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        assert response.status_code == 500

    def test_login_1_success(self, test_app):
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

    def test_login_2_success(self, test_app):
        login_schema = LoginSchema(
            email=RegisterUser2.email, password=RegisterUser1.password
        )
        response = test_app.do_request(
            "POST",
            ApiServices.APP_LOGIN,
            data=login_schema.model_dump(),
        )

        if response.status_code == 200:
            test_app.tokens[f"{RegisterUser2.name}_{RegisterUser2.surname}"] = (
                response.json().get("access_token")
            )
