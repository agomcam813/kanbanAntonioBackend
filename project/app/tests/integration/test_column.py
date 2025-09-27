import pytest
from requests import Response

from app.schemas.column_schema import ColumnInputSchema
from app.tests.conftest import TestAPP
from app.tests.constants import ColumnCreate, ApiServices


@pytest.mark.usefixtures("test_app")
class TestColumn:
    @staticmethod
    def create_column(column_schema: ColumnInputSchema, test_app: TestAPP) -> Response:
        return test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_COLUMN,
            data=column_schema.model_dump(),
        )

    @staticmethod
    def get_all_columns(board_id: int, test_app: TestAPP) -> Response:
        return test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_COLUMN_GET_ALL.format(board_id=board_id)
        )

    def test_get_all_columns_empty(self, test_app):
        response = self.get_all_columns(test_app.board_1.id, test_app)
        assert response.status_code == 200

    def test_create_column_success(self, test_app):
        column_schema = ColumnInputSchema(**ColumnCreate.__dict__)
        response = self.create_column(column_schema, test_app)
        assert response.status_code == 200

    def test_create_column_exist(self, test_app):
        column_schema = ColumnInputSchema(**ColumnCreate.__dict__)
        response = self.create_column(column_schema, test_app)
        assert response.status_code == 400

    def test_get_all_columns(self, test_app):
        response = self.get_all_columns(test_app.board_1.id, test_app)
        assert response.status_code == 200
