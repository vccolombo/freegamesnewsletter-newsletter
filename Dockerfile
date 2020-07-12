FROM python:3.8-slim-buster

RUN python -m pip install --upgrade pip

COPY requirements.txt /
RUN buildDeps='gcc libc-dev build-essential' \
    && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
    && python -m pip install -r /requirements.txt \
    && apt-get purge -y --auto-remove $buildDeps \
    && rm -rf /var/lib/apt/lists/*

COPY src/ /app
WORKDIR /app

CMD ["python", "main.py"]