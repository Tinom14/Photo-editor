from worker_service.src.usecases.abstract_task_service import AbstractTaskService
import json
import base64
import uuid
from io import BytesIO
from PIL import Image
from worker_service.src.filters.filters import apply_filter
from worker_service.src.repository.abstract_task_sender import AbstractTaskSender
from prometheus_client import Counter, Histogram
import time
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NUMBER_FILTERS = Counter(
    "number_of_filters",
    "Number of filters used",
    ["filter"]
)

EXECUTION_TIME = Histogram(
    "execution_time",
    "Execution time",
    ["filter"],
    buckets=[0.1, 0.3, 0.5, 1.0, 2.0, 5.0]
)


class TaskService(AbstractTaskService):
    def __init__(self, task_sender: AbstractTaskSender):
        self._result_sender = task_sender

    async def process_task(self, body: bytes):
        try:
            start_time = time.time()
            logger.info(f"Начало обработки задачи: {body[:100]}...")
            task = json.loads(body.decode())
            task_id = uuid.UUID(task["task_id"])
            filter_obj = task["filter"]
            encoded_image = task["image"]

            image_data = base64.b64decode(encoded_image)
            image = Image.open(BytesIO(image_data))

            processed_image = apply_filter(image, filter_obj)

            output = BytesIO()
            processed_image.save(output, format="PNG")
            result_bytes = output.getvalue()

            logger.info(f"Отправка результата для task_id: {task_id}")
            await self._result_sender.save_result(task_id, result_bytes)
            NUMBER_FILTERS.labels(filter_obj["name"]).inc()
            EXECUTION_TIME.labels(filter_obj["name"]).observe(time.time() - start_time)
            logger.info(f"Результат отправлен для task_id: {task_id}")

        except Exception as e:
            logger.info(f"Ошибка в process_task: {e}")
            raise