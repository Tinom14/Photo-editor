from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
import uuid
from shared.postgres_connection.models.task import Task

from worker_service.src.repository.abstract_task_sender import AbstractTaskSender


class TaskSender(AbstractTaskSender):
    def __init__(self, db):
        self.db = db

    async def save_result(self, task_id: uuid.UUID, image_data: bytes):
        try:
            await self.db.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(
                    status="Ready",
                    result=image_data
                )
            )
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e