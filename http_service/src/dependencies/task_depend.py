from fastapi import Depends
from http_service.src.repository.postgres.task_repository import TaskRepository
from http_service.src.repository.abstract_task_repository import AbstractTaskRepository
from http_service.src.repository.task_sender import TaskSender
from http_service.src.repository.rabbit_mq.task_sender import RabbitMQProducer
from http_service.src.usecases.abstract_task_service import AbstractTaskService
from http_service.src.usecases.service.task_service import TaskService
from sqlalchemy.ext.asyncio import AsyncSession
from shared.postgres_connection.postgres import get_db

task_sender = RabbitMQProducer()

async def get_task_repo(db: AsyncSession = Depends(get_db)) -> AbstractTaskRepository:
    return TaskRepository(db)

async def get_task_sender():
    return task_sender

async def get_task_service(
    repo: AbstractTaskRepository = Depends(get_task_repo), sender: TaskSender = Depends(get_task_sender)
) -> AbstractTaskService:
    return TaskService(repo, sender)