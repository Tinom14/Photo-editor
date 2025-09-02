from sqlalchemy.ext.asyncio import AsyncSession
from worker_service.src.repository.postgres.task import TaskSender
from worker_service.src.repository.abstract_task_sender import AbstractTaskSender
from worker_service.src.usecases.service.task_service import TaskService
from worker_service.src.usecases.abstract_task_service import AbstractTaskService

def get_task_sender(db: AsyncSession) -> AbstractTaskSender:
    return TaskSender(db)

def get_task_service(db: AsyncSession) -> AbstractTaskService:
    sender = get_task_sender(db)
    return TaskService(sender)
