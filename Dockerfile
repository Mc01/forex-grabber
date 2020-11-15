FROM python:3.8

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements/requirements.txt ./requirements.txt
COPY requirements/requirements.dev.txt ./requirements.dev.txt
RUN pip install -r requirements.txt -r requirements.dev.txt
