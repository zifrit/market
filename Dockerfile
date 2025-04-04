FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk update \
    && apk add --no-cache \
    curl \
    && rm -rf /var/cache/apk/* \
    && curl -sSL 'https://install.python-poetry.org' | python3 - --version 1.7.1

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-ansi --no-interaction --no-dev

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver"]