import pytest

from app.schemas.task_schema import TaskInputSchema
from app.tests.constants import ApiServices, TaskCreate


@pytest.mark.usefixtures("test_app")
class TestTask:
    def test_create_task(self, test_app):
        task_schema = TaskInputSchema(**TaskCreate.__dict__)
        response = test_app.do_request_with_role(
            "USER_1",
            "POST",
            ApiServices.APP_TASK,
            data=task_schema.model_dump(),
        )
        assert response.status_code == 200
