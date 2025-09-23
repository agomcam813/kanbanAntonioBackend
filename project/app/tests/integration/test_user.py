import pytest

from app.schemas.user_schema import UserUpdateSchema
from app.tests.constants import ApiServices, RegisterUser1, UpdateUser1


@pytest.mark.usefixtures("test_app")
class TestUser:

    def test_get_me_successfully(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1", "GET", ApiServices.APP_GET_ME_USER
        )

        assert response.status_code == 200

    def test_update_me_successfully(self, test_app):
        update_schema = UserUpdateSchema(**UpdateUser1.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_UPDATE_ME_USER,
            data=update_schema.model_dump(),
        )
        assert response.status_code == 200
        assert response.json()["name"] != RegisterUser1.name
        assert response.json()["surname"] != RegisterUser1.surname

    def test_delete_user_1(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_DELETE_ME_USER,
        )
        assert response.status_code == 200
        test_app.tokens.pop("USER_1")

    def test_delete_user_2(self, test_app):
        response = test_app.do_request_with_role(
            "USER_2",
            "DELETE",
            ApiServices.APP_DELETE_ME_USER,
        )
        assert response.status_code == 200
        test_app.tokens.pop("USER_2")
