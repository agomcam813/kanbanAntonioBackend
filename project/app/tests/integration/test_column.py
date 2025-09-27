import pytest
from requests import Response

from app.schemas.column_schema import (
    ColumnInputSchema,
    ColumnUpdateNameSchema,
    ColumnUpdateOrderSchema,
)
from app.tests.conftest import TestAPP
from app.tests.constants import (
    ApiServices,
    ColumnChangeDifferentName,
    ColumnChangeSameName,
    ColumnCreate1,
    ColumnCreate2,
    ColumnMove,
)


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
            "USER_1", "GET", ApiServices.APP_COLUMN_GET_ALL.format(board_id=board_id)
        )

    def test_get_all_columns_empty(self, test_app):
        response = self.get_all_columns(test_app.board_1.id, test_app)
        assert response.status_code == 200

    def test_create_column_success_1(self, test_app):
        column_schema = ColumnInputSchema(**ColumnCreate1.__dict__)
        response = self.create_column(column_schema, test_app)
        assert response.status_code == 200

    def test_create_column_success_2(self, test_app):
        column_schema = ColumnInputSchema(**ColumnCreate2.__dict__)
        response = self.create_column(column_schema, test_app)
        assert response.status_code == 200

    def test_create_column_exist(self, test_app):
        column_schema = ColumnInputSchema(**ColumnCreate1.__dict__)
        response = self.create_column(column_schema, test_app)
        assert response.status_code == 400

    def test_get_all_columns(self, test_app):
        response = self.get_all_columns(test_app.board_1.id, test_app)
        assert response.status_code == 200

    def test_change_column_same_name(self, test_app):
        column_schema = ColumnUpdateNameSchema(**ColumnChangeSameName.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_COLUMN_CHANGE_NAME,
            data=column_schema.model_dump(),
        )

        assert response.status_code == 400

    def test_change_column_different_name(self, test_app):
        column_schema = ColumnUpdateNameSchema(**ColumnChangeDifferentName.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_COLUMN_CHANGE_NAME,
            data=column_schema.model_dump(),
        )

        assert response.status_code == 200

    def test_move_column(self, test_app):
        column_schema = ColumnUpdateOrderSchema(**ColumnMove.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "PUT",
            ApiServices.APP_COLUMN_MOVE,
            data=column_schema.model_dump(),
        )
        assert response.status_code == 200
