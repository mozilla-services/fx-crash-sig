FROM python:3.8.5-slim@sha256:9c84459051ee7e9d386b24ee5468352d52b6789a5d4a8cf6a649a8a1c6ad5636

# https://github.com/mozilla-services/Dockerflow/blob/master/docs/building-container.md
ARG USER_ID="10001"
ARG GROUP_ID="10001"

ENV HOME=/app
RUN groupadd --gid ${GROUP_ID} app && \
    useradd --uid ${USER_ID} --gid ${GROUP_ID} --home-dir /app --create-home app

RUN apt-get update && \
    apt-get install -y build-essential 

WORKDIR /app

COPY requirements.dev.txt /app/
RUN pip install --no-cache-dir --upgrade 'pip>=8' && \
    pip install --no-cache-dir -r requirements.dev.txt && \
    pip check --no-cache-dir --disable-pip-version-check

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

COPY . /app

RUN pip install --no-cache-dir /app

RUN chown app:app /app/

USER app
