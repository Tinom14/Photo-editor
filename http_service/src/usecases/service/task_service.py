import uuid

from http_service.src.usecases.abstract_task_service import AbstractTaskService
from http_service.src.repository.abstract_task_repository import AbstractTaskRepository
from http_service.src.repository.task_sender import TaskSender
from shared.schemas.schemas import FilterParameters


class TaskService(AbstractTaskService):
    def __init__(self, tasks_repo: AbstractTaskRepository, sender: TaskSender):
        self.tasks_repo: AbstractTaskRepository = tasks_repo
        self.sender: TaskSender = sender

    async def create_task(self, image_data: bytes, task_filter: FilterParameters) -> uuid.UUID:
        task = await self.tasks_repo.create_task(uuid.uuid4())
        await self.sender.send_task(
            task_id=task.id,
            image_data=image_data,
            filter_obj=task_filter.model_dump()
        )
        return task.id

    async def get_task_status(self, task_id: uuid.UUID) -> str:
        task = await self.tasks_repo.get_task(task_id)
        return task.status

    async def get_task_result(self, task_id: uuid.UUID) -> bytes:
        task = await self.tasks_repo.get_task(task_id)
        return task.result
