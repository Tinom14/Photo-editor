FROM python:3.13.0-slim AS build

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

WORKDIR /build

COPY worker_service/requirements-second.txt requirements.txt

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY ../shared ./shared
COPY worker_service/ ./worker_service/

FROM python:3.13.0-slim AS runner

WORKDIR /app

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/app:/usr/local/lib/python3.13/site-packages

COPY --from=build /install /usr/local
COPY --from=build /build/worker_service/ ./worker_service/
COPY --from=build /build/shared/ ./shared/

CMD ["python", "-m", "worker_service.src.main", "--config", "worker_service/src/config/config.yml"]
