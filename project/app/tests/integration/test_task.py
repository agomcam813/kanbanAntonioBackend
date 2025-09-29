import pytest
from requests import Response

from app.schemas.task_schema import TaskInputSchema
from app.tests.conftest import TestAPP
from app.tests.constants import ApiServices, TaskCreate, TaskCreateErrorColumnId


@pytest.mark.usefixtures("test_app")
class TestTask:
    @staticmethod
    def create_task(
        user: str, task_schema: TaskInputSchema, test_app: TestAPP
    ) -> Response:
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=task_schema.model_dump(),
        )
        return response

    def test_create_task(self, test_app):
        task_schema = TaskInputSchema(**TaskCreate.__dict__)
        response = self.create_task("USER_1", task_schema, test_app)
        assert response.status_code == 200

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
