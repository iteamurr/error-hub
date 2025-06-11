FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry --no-cache-dir && \
    poetry install --no-root --without dev

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.wsgi:app", "--workers", "4"]
