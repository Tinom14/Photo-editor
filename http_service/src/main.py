from fastapi import FastAPI
from http_service.src.config.config import AppConfig
from http_service.src.api import task, auth
from http_service.src.repository.rabbit_mq.task_sender import RabbitMQProducer
from shared.postgres_connection.postgres import create_db_and_tables
from shared.redis_connection.config import redis_config
from shared.redis_connection import config as redis_config_module
import redis.asyncio as redis
from contextlib import asynccontextmanager
import uvicorn
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
rabbit_producer = RabbitMQProducer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запускается: Инициализация ресурсов...")

    try:
        logger.info("Создание таблиц в базе данных")
        await create_db_and_tables()

        logger.info("Инициализация RabbitMQProducer")
        await rabbit_producer._get_channel()

        logger.info("Инициализация Redis клиента")
        redis_client = redis.Redis(
            host=redis_config.host,
            port=redis_config.port,
            db=redis_config.db,
            password=redis_config.password or None
        )
        await redis_client.ping()
        redis_config_module.redis_client = redis_client

        logger.info("Все компоненты инициализированы успешно")
        yield

    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
        raise

    finally:
        try:
            logger.info("Закрытие RabbitMQProducer")
            await rabbit_producer.close()
        except Exception as e:
            logger.error(f"Ошибка при завершении RabbitMQ: {e}")

        try:
            if redis_config_module.redis_client:
                logger.info("Закрытие Redis клиента")
                await redis_config_module.redis_client.close()
        except Exception as e:
            logger.error(f"Ошибка при завершении Redis: {e}")
app = FastAPI(lifespan=lifespan)

app.include_router(task.router)
app.include_router(task.router2)
app.include_router(auth.router)



if __name__ == "__main__":
    args = AppConfig.parse_flags()
    cfg = AppConfig.must_load(args.config)
    host, port = cfg.address.split(":")

    host = args.host if args.host is not None else host
    port = args.port if args.port is not None else port

    logging.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=int(port))
