from app.schemas.auth_schema import RegisterSchema
from app.tests.constants import ApiServices, RegisterUser1
import pytest


@pytest.mark.usefixtures("test_app")
class TestAuth:
    def test_register_success(self, test_app):
        register_schema = RegisterSchema(**RegisterUser1.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        print(response.text)
        assert response.status_code == 200

    def test_register_failure(self, test_app):
        register_schema = RegisterSchema(**RegisterUser1.__dict__)
        response = test_app.do_request(
            "POST",
            ApiServices.APP_REGISTER,
            data=register_schema.model_dump(),
        )
        print(response.text)
        assert response.status_code == 500
        