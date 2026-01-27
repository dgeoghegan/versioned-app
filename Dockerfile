# syntax=docker/dockerfile:1

FROM python:3.11.8-slim-bookworm

ENV APP_NAME=versioned-app
ENV PORT=8080
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Non-root user
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin appuser

WORKDIR /app
COPY app.py /app/app.py

USER 10001:10001
EXPOSE 8080

ENTRYPOINT ["python", "/app/app.py"]
