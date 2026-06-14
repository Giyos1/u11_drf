FROM python:3.13-slim

LABEL maintainer="ism@email.com"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Default: ASGI server (Channels/websockets). Overridden per service in docker-compose.
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]