FROM python:3.5

# Path: /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

