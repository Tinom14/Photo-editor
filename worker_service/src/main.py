import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from worker_service.src.api.rabbit_mq import RabbitMQConsumer
from worker_service.src.dependencies.dependencies import get_task_service
from shared.postgres_connection.postgres import get_db
from prometheus_client import start_http_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_http_server(8002)
    logger.info("Prometheus metrics server started on port 8001")
    async for db in get_db():
        task_service = get_task_service(db)
        consumer = RabbitMQConsumer(service=task_service)
        await consumer.consume_tasks()
        break

    try:
        yield
    finally:
        try:
            await consumer.close()
        except Exception as e:
            logger.exception("Ошибка при закрытии RabbitMQ: %s", e)


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn
    from worker_service.src.config.config import AppConfig

    args = AppConfig.parse_flags()
    cfg = AppConfig.must_load(args.config)
    host, port = cfg.address.split(":")

    host = args.host if args.host is not None else host
    port = args.port if args.port is not None else port

    logging.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=int(port))
