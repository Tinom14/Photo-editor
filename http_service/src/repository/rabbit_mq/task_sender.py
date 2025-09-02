import uuid
import aio_pika
import json
from shared.rabbit_connection.config import rabbitmq_config
from http_service.src.repository.task_sender import TaskSender
import base64


class RabbitMQProducer(TaskSender):
    def __init__(self):
        self._connection = None
        self._channel = None
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
            await self._channel.declare_queue(self.config.queue, durable=True)
        return self._channel

    async def send_task(self, task_id: uuid.UUID, image_data: bytes, filter_obj: dict):
        channel = await self._get_channel()
        encoded_image = base64.b64encode(image_data).decode()
        message_body = json.dumps({
            "task_id": str(task_id),
            "filter": filter_obj,
            "image": encoded_image
        }).encode()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
            ),
            routing_key=self.config.queue
        )

    async def close(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()