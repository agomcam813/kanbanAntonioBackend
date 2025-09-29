import pytest
from requests import Response

from app.schemas.task_schema import (
    TaskInputSchema,
    TaskOutputSchema,
    TaskUpdateOrderSchema,
    TaskUpdateSchema,
)
from app.tests.conftest import TestAPP
from app.tests.constants import (
    ApiServices,
    TaskCreate,
    TaskCreateErrorColumnId,
    TaskMove,
    TaskUpdate,
    TaskUpdateErrorTask,
)


@pytest.mark.usefixtures("test_app")
class TestTask:
    @staticmethod
    def create_task(
        user: str, task_schema: TaskInputSchema, test_app: TestAPP
    ) -> Response:
        response = test_app.do_request_with_role(
            user,
            "POST",
            ApiServices.APP_TASK,
            data=task_schema.model_dump(),
        )
        return response

    @staticmethod
    def update_task(
        user: str, task_schema: TaskUpdateSchema, test_app: TestAPP
    ) -> Response:
        response = test_app.do_request_with_role(
            user,
            "PUT",
            ApiServices.APP_TASK_UPDATE,
            data=task_schema.model_dump(),
        )
        return response

    def test_get_columns_with_tasks_none_exist_task(self, test_app):
        response = self.get_task_with_columns(test_app)
        assert response.status_code == 200

    @staticmethod
    def get_task_with_columns(test_app: TestAPP) -> Response:
        response = test_app.do_request_with_role(
            "USER_1",
            "GET",
            ApiServices.APP_TASK_GET_COLUMNS_WITH_TASKS.format(
                board_id=test_app.board_1.id
            ),
        )
        return response

    @staticmethod
    def update_order_task(
        user: str, task_schema: TaskUpdateOrderSchema, test_app: TestAPP
    ) -> Response:
        response = test_app.do_request_with_role(
            user,
            "PUT",
            ApiServices.APP_TASK_MOVE,
            data=task_schema.model_dump(),
        )
        return response

    @staticmethod
    def remove_task(user: str, test_app: TestAPP) -> Response:
        response = test_app.do_request_with_role(
            user,
            "DELETE",
            ApiServices.APP_TASK_DELETE.format(task_id=test_app.task_1.id),
        )
        return response

    def test_create_task(self, test_app):
        task_schema = TaskInputSchema(**TaskCreate.__dict__)
        response = self.create_task("USER_1", task_schema, test_app)
        assert response.status_code == 200
        test_app.task_1 = TaskOutputSchema(**response.json())

    def test_create_task_same_name(self, test_app):
        task_schema = TaskInputSchema(**TaskCreate.__dict__)
        response = self.create_task("USER_1", task_schema, test_app)
        assert response.status_code == 400

    def test_create_task_none_exist_column(self, test_app):
        task_schema = TaskInputSchema(**TaskCreateErrorColumnId.__dict__)
        response = self.create_task("USER_1", task_schema, test_app)
        assert response.status_code == 404

    def test_create_task_user_not_column(self, test_app):
        task_schema = TaskInputSchema(**TaskCreateErrorColumnId.__dict__)
        response = self.create_task("USER_2", task_schema, test_app)
        assert response.status_code == 404

    def test_get_columns_with_tasks_exist_task(self, test_app):
        response = self.get_task_with_columns(test_app)
        assert response.status_code == 200

    def test_update_task(self, test_app):
        task_schema = TaskUpdateSchema(**TaskUpdate.__dict__)
        response = self.update_task("USER_1", task_schema, test_app)
        assert response.status_code == 200
        test_app.task_1 = TaskOutputSchema(**response.json())

    def test_update_task_none_exist_task(self, test_app):
        task_schema = TaskUpdateSchema(**TaskUpdateErrorTask.__dict__)
        response = self.update_task("USER_1", task_schema, test_app)
        assert response.status_code == 404

    def test_update_task_none_user_in_board(self, test_app):
        task_schema = TaskUpdateSchema(**TaskUpdate.__dict__)
        response = self.update_task("USER_2", task_schema, test_app)
        assert response.status_code == 403

    def test_move_task(self, test_app):
        task_schema = TaskUpdateOrderSchema(**TaskMove.__dict__)
        response = self.update_order_task("USER_1", task_schema, test_app)

        assert response.status_code == 200

    def test_move_task_none_exist_task(self, test_app):
        task_schema = TaskUpdateOrderSchema(**TaskMove.__dict__)
        task_schema.id = 99
        response = self.update_order_task("USER_1", task_schema, test_app)

        assert response.status_code == 404

    def test_move_task_user_not_column(self, test_app):
        task_schema = TaskUpdateOrderSchema(**TaskMove.__dict__)
        response = self.update_order_task("USER_2", task_schema, test_app)

        assert response.status_code == 403

    def test_remove_task(self, test_app):
        response = self.remove_task("USER_1", test_app)
        assert response.status_code == 200

    def test_remove_task_none_exist(self, test_app):
        response = self.remove_task("USER_1", test_app)
        assert response.status_code == 404
