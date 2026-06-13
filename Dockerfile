FROM python:3.13-slim

LABEL maintainer="ism@email.com"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ARG BUILD_VERSION=latest
RUN echo "Version: $BUILD_VERSION"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]