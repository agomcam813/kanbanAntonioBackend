# import pytest
# from app.tests.constants import ApiServices
#
# @pytest.mark.usefixtures("test_app")
# class TestUser:
#     @pytest.mark.asyncio
#     async def test_delete_user(self, test_app):
#         response = await test_app.do_request_with_role(
#             "USER_1",
#             "DELETE",
#             ApiServices.APP_DELETE_USER,
#         )
#         assert response.status_code == 200