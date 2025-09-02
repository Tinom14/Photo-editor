import aio_pika
import logging
from worker_service.src.usecases.abstract_task_service import AbstractTaskService
from shared.rabbit_connection.config import rabbitmq_config

logger = logging.getLogger(__name__)

class RabbitMQConsumer:
    def __init__(self, service: AbstractTaskService):
        self._connection = None
        self._channel = None
        self._queue = None
        self.service = service
        self.config = rabbitmq_config

    async def _get_channel(self):
        if not self._channel or self._channel.is_closed:
            if not self._connection or self._connection.is_closed:
                self._connection = await aio_pika.connect_robust(
                    host=self.config.host,
                    port=self.config.port,
                    login=self.config.username,
                    password=self.config.password,
                )
            self._channel = await self._connection.channel()
            self._queue = await self._channel.declare_queue(
                self.config.queue,
                durable=True
            )
        return self._channel, self._queue

    async def consume_tasks(self):
        channel, queue = await self._get_channel()

        async def on_message(message: aio_pika.IncomingMessage):
            async with message.process():
                try:
                    await self.service.process_task(message.body)
                    logger.info(f"Задача {message.delivery_tag} обработана")
                except Exception as e:
                    logger.error(f"Ошибка обработки задачи: {e}")

        await queue.consume(on_message)
        logger.info(f"Worker слушает очередь [{self.config.queue}]")

    async def close(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
