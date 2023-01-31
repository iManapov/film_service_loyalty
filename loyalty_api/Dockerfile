FROM python:3.10.6-slim

EXPOSE 8009

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  apt-get update \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "main:app", "--workers", "4", "--worker-class", \
            "uvicorn.workers.UvicornH11Worker", "--bind", "0.0.0.0:8009"]
