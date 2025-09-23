import pytest
from app.tests.constants import ApiServices


@pytest.mark.usefixtures("test_app")
class TestUser:

    def test_delete_user(self, test_app):
        response = test_app.do_request_with_role(
            "USER_1",
            "DELETE",
            ApiServices.APP_DELETE_USER,
        )
        assert response.status_code == 200
        test_app.tokens.pop("USER_1")
